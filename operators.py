"""
Blender Operator Definition
Handles the "Convert to Unity" operators – accessible via File > Export only.
"""

import bpy
import os
from pathlib import Path
from . import parser, converter, exporter, utils

# Load node mappings from JSON at addon startup.
# Wrapped in a try/except so a missing or malformed JSON does not prevent
# the addon from registering — operators will report the error at execute time.
try:
    NODE_MAPPING = utils.load_node_mappings()
except Exception as _load_err:
    NODE_MAPPING = {}
    import sys
    print(f"[Unity Shader Converter] WARNING: Could not load node_mappings.json: {_load_err}",
          file=sys.stderr)


# ── Shared helpers ─────────────────────────────────────────────────────────────

def _sanitize_name(name: str) -> str:
    """Strip file extension then replace path-unsafe characters."""
    name = str(name)
    name = os.path.splitext(name)[0]
    for ch in r'\/:*?"<>|. ':
        name = name.replace(ch, '_')
    return name.strip('_') or "Exported"


def _collect_all_materials():
    """Return every unique node-based material used by mesh objects in the scene."""
    seen = set()
    materials = []
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and obj.data:
            for slot in obj.material_slots:
                mat = slot.material
                if mat and mat.use_nodes and mat.name not in seen:
                    seen.add(mat.name)
                    materials.append(mat)
    return materials


def _analyze_conversion(blender_data: dict) -> dict:
    """Analyse a parsed shader and return a stats dict suitable for the README."""
    from . import socket_handler

    analysis = {
        'material_name': blender_data.get('name', ''),
        'total_nodes': len(blender_data['nodes']),
        'direct_nodes': 0,
        'decompose_nodes': 0,
        'approximation_nodes': 0,
        'incompatible_nodes': [],
        'type_mismatches': [],
        'conversion_notes': [],
        'approximation_details': [],
        'success_rate': 0,
    }

    APPROX_STRATEGIES = {
        'approximation', 'blend_mapping', 'normal_mapping',
        'uv_mapping', 'texture_reference', 'attribute_mapping', 'procedural_texture',
    }

    for node_data in blender_data['nodes']:
        node_type = node_data['blender_type']
        node_map = NODE_MAPPING.get(node_type, {})
        strategy = node_map.get('strategy', 'incompatible')

        if strategy == 'direct':
            analysis['direct_nodes'] += 1
        elif strategy == 'decompose':
            analysis['decompose_nodes'] += 1
        elif strategy in APPROX_STRATEGIES:
            analysis['approximation_nodes'] += 1
            unity_name = node_map.get('unity_name', 'Unknown')
            # For blend_mapping nodes, include the active blend mode in the detail
            props = node_data.get('properties', {})
            blend = props.get('blend_mode') or props.get('blend_type', '')
            detail = f"{node_data['name']} ({node_type}) → {unity_name}"
            if blend and blend not in ('MIX', ''):
                detail += f" [{blend} mode]"
            analysis['approximation_details'].append(detail)
        else:
            analysis['incompatible_nodes'].append({
                'name': node_data['name'],
                'type': node_type,
                'reason': node_map.get('description', 'No direct Unity equivalent'),
            })
            analysis['conversion_notes'].append(
                f"{node_data['name']} ({node_type}) - No direct Unity equivalent"
            )

    for conn in blender_data['connections']:
        ok, _ = socket_handler.SocketTypeHandler.check_compatibility(
            conn['from_type'], conn['to_type']
        )
        if not ok:
            analysis['type_mismatches'].append({
                'from': f"{conn['from_node']}.{conn['from_socket']} ({conn['from_type']})",
                'to':   f"{conn['to_node']}.{conn['to_socket']} ({conn['to_type']})",
            })
            analysis['conversion_notes'].append(
                f"Type mismatch: {conn['from_type']} -> {conn['to_type']}"
            )

    convertible = (analysis['direct_nodes'] + analysis['decompose_nodes']
                   + analysis['approximation_nodes'])
    if analysis['total_nodes']:
        analysis['success_rate'] = int(convertible / analysis['total_nodes'] * 100)

    return analysis


def _merge_analysis(analyses: list) -> dict:
    """Merge per-material analysis dicts into one for a combined README."""
    names = [a['material_name'] for a in analyses]
    # Cap the title to avoid an unreadably long README header
    if len(names) <= 5:
        combined_name = ', '.join(names)
    else:
        combined_name = ', '.join(names[:5]) + f' … and {len(names) - 5} more'

    merged = {
        'material_name': combined_name,
        'total_nodes':          sum(a['total_nodes']          for a in analyses),
        'direct_nodes':         sum(a['direct_nodes']         for a in analyses),
        'decompose_nodes':      sum(a['decompose_nodes']      for a in analyses),
        'approximation_nodes':  sum(a['approximation_nodes']  for a in analyses),
        'incompatible_nodes':   [],
        'type_mismatches':      [],
        'conversion_notes':     [],
        'approximation_details':[],
        'success_rate':         0,
    }
    for a in analyses:
        merged['incompatible_nodes'].extend(a['incompatible_nodes'])
        merged['type_mismatches'].extend(a['type_mismatches'])
        merged['conversion_notes'].extend(a['conversion_notes'])
        merged['approximation_details'].extend(a['approximation_details'])

    if merged['total_nodes']:
        convertible = (merged['direct_nodes'] + merged['decompose_nodes']
                       + merged['approximation_nodes'])
        merged['success_rate'] = int(convertible / merged['total_nodes'] * 100)
    return merged


def _export_collection_as_fbx(collection, export_dir: str) -> bool:
    """
    Duplicate every mesh/armature/empty in collection, zero their XY,
    export as a single FBX, then clean up duplicates.
    Returns True on success.
    """
    bpy.ops.object.select_all(action='DESELECT')

    duplicated_objects = []
    for obj in list(collection.all_objects):
        if obj and obj.type in {'MESH', 'EMPTY', 'ARMATURE'}:
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.duplicate()
            dup = bpy.context.active_object
            dup.location.x = 0
            dup.location.y = 0
            duplicated_objects.append(dup)
            obj.select_set(False)

    if not duplicated_objects:
        print(f"No exportable objects in collection '{collection.name}'")
        return False

    temp_col = bpy.data.collections.new(name=f"Temp_{collection.name}")
    bpy.context.scene.collection.children.link(temp_col)
    for obj in duplicated_objects:
        # Move the duplicate exclusively into the temp collection so it doesn't
        # appear twice in the scene hierarchy during export
        if obj.name in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.unlink(obj)
        temp_col.objects.link(obj)

    safe_name = _sanitize_name(collection.name)
    fbx_path = os.path.join(export_dir, f"{safe_name}.fbx")

    bpy.ops.object.select_all(action='DESELECT')
    for obj in duplicated_objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = duplicated_objects[0]

    bpy.ops.export_scene.fbx(
        filepath=fbx_path,
        use_selection=True,
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_ALL',
        object_types={'MESH', 'ARMATURE', 'EMPTY'},
        bake_space_transform=True,
        mesh_smooth_type='OFF',
        add_leaf_bones=False,
        axis_forward='-Z',
        axis_up='Y',
        # Blender 5.0 compatibility - remove potentially unsupported params
    )

    for obj in duplicated_objects:
        bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.collections.remove(temp_col)

    print(f"Exported FBX: {fbx_path}")
    return True


# ── Operators ──────────────────────────────────────────────────────────────────

class SHADER_OT_convert_to_unity(bpy.types.Operator):
    """Convert ALL node-based materials in the scene to Unity shader graphs"""
    bl_idname = "shader.convert_to_unity"
    bl_label = "Convert to Unity"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(
        name="Output Directory",
        description="Directory to export converted shaders",
        subtype='DIR_PATH',
    )
    filter_folder: bpy.props.BoolProperty(default=True, options={'HIDDEN'})

    def execute(self, context):
        if not NODE_MAPPING:
            self.report({'ERROR'}, "node_mappings.json failed to load. Check the console.")
            return {'CANCELLED'}

        all_materials = _collect_all_materials()
        if not all_materials:
            self.report({'ERROR'}, "No node-based materials found in scene")
            return {'CANCELLED'}

        try:
            exp = exporter.UnityExporter(self.filepath)
            exp.setup_folders()

            converted, failed, all_analysis = 0, 0, []

            for mat in all_materials:
                print(f"\nParsing shader: {mat.name}")
                try:
                    blender_data = parser.BlenderShaderParser(mat).parse()
                    unity_graph = converter.ShaderGraphConverter(blender_data, NODE_MAPPING).convert()
                    exp.export_shader_graph(unity_graph, mat.name)
                    exp.export_material(mat.name, mat.name + "_Material")
                    all_analysis.append(_analyze_conversion(blender_data))
                    converted += 1
                except Exception as e:
                    print(f"Failed to convert {mat.name}: {e}")
                    import traceback; traceback.print_exc()
                    failed += 1

            if all_analysis:
                exp.export_conversion_readme(_merge_analysis(all_analysis))

            self.report(
                {'INFO'},
                f"Converted {converted} material(s) to {self.filepath}"
                + (f" ({failed} failed)" if failed else ""),
            )
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Conversion failed: {e}")
            import traceback; traceback.print_exc()
            return {'CANCELLED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class SHADER_OT_export_collections_fbx(bpy.types.Operator):
    """Export each top-level collection as a separate FBX file"""
    bl_idname = "shader.export_collections_fbx"
    bl_label = "Export Collections as FBX"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(
        name="Output Directory",
        description="Directory to export FBX files",
        subtype='DIR_PATH',
    )
    filter_folder: bpy.props.BoolProperty(default=True, options={'HIDDEN'})

    def execute(self, context):
        # Handle unsaved blend files - use temp directory as fallback
        if self.filepath:
            export_dir = self.filepath
        elif bpy.data.filepath:
            export_dir = os.path.dirname(bpy.data.filepath)
        else:
            import tempfile
            export_dir = os.path.join(tempfile.gettempdir(), "UnityExport")
        
        if not export_dir:
            self.report({'ERROR'}, "Please save the Blender file first or pick a directory.")
            return {'CANCELLED'}

        collections = list(bpy.context.scene.collection.children)
        if not collections:
            self.report({'WARNING'}, "No top-level collections found.")
            return {'CANCELLED'}

        count = sum(1 for col in collections if _export_collection_as_fbx(col, export_dir))
        self.report({'INFO'}, f"Exported {count} collection(s) as FBX.")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class SHADER_OT_convert_and_export_all(bpy.types.Operator):
    """Convert ALL materials AND export ALL collections as FBX in one operation"""
    bl_idname = "shader.convert_and_export_all"
    bl_label = "Convert & Export All (Unity)"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(
        name="Output Directory",
        description="Parent directory - a named subfolder will be created inside",
        subtype='DIR_PATH',
    )
    filter_folder: bpy.props.BoolProperty(default=True, options={'HIDDEN'})

    def execute(self, context):
        # Handle unsaved blend files - use temp directory as fallback
        if self.filepath:
            export_dir = self.filepath
        elif bpy.data.filepath:
            export_dir = os.path.dirname(bpy.data.filepath)
        else:
            import tempfile
            export_dir = os.path.join(tempfile.gettempdir(), "UnityExport")
        
        if not export_dir:
            self.report({'ERROR'}, "Please save the Blender file first or pick a directory.")
            return {'CANCELLED'}

        # Build a clean subfolder name from the .blend file stem (no extension)
        # Use a safe default if blend file is unsaved
        if bpy.data.filepath:
            blend_stem = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
        else:
            blend_stem = "UnityExport"
        safe_folder = _sanitize_name(blend_stem) or "UnityExport"
        export_path = os.path.join(export_dir, safe_folder)

        try:
            # ── 1. Models: export every top-level collection as FBX ──────────
            models_folder = os.path.join(export_path, "Models")
            os.makedirs(models_folder, exist_ok=True)

            fbx_count = 0
            for col in bpy.context.scene.collection.children:
                if _export_collection_as_fbx(col, models_folder):
                    fbx_count += 1

            # ── 2. Shaders / Materials: convert ALL unique materials ──────────
            all_materials = _collect_all_materials()
            mat_count, mat_failed, all_analysis = 0, 0, []

            if all_materials:
                # UnityExporter.setup_folders() creates Shaders/, Materials/, Textures/
                exp = exporter.UnityExporter(export_path)
                exp.setup_folders()

                for mat in all_materials:
                    print(f"\nParsing shader: {mat.name}")
                    try:
                        blender_data = parser.BlenderShaderParser(mat).parse()
                        unity_graph = converter.ShaderGraphConverter(
                            blender_data, NODE_MAPPING
                        ).convert()
                        safe_mat = _sanitize_name(mat.name)
                        exp.export_shader_graph(unity_graph, safe_mat)
                        exp.export_material(safe_mat, safe_mat + "_Material")
                        all_analysis.append(_analyze_conversion(blender_data))
                        mat_count += 1
                    except Exception as e:
                        print(f"Failed to convert {mat.name}: {e}")
                        import traceback; traceback.print_exc()
                        mat_failed += 1

                if all_analysis:
                    exp.export_conversion_readme(_merge_analysis(all_analysis))

            # ── Report ────────────────────────────────────────────────────────
            parts = []
            if fbx_count:
                parts.append(f"{fbx_count} FBX file(s)")
            if mat_count:
                parts.append(f"{mat_count} shader(s)")
            if mat_failed:
                parts.append(f"{mat_failed} shader(s) failed - check console")

            msg = "Exported to {}: {}".format(
                export_path, ", ".join(parts) if parts else "nothing exported"
            )
            self.report({'INFO'} if parts else {'WARNING'}, msg)
            print(f"\n{msg}\n")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Export failed: {e}")
            print(f"Error: {e}")
            import traceback; traceback.print_exc()
            return {'CANCELLED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


# ── File > Export menu entries only ───────────────────────────────────────────

def export_menu_func(self, context):
    """Adds three entries to File > Export"""
    self.layout.separator()
    self.layout.operator(
        SHADER_OT_convert_and_export_all.bl_idname,
        text="Convert & Export All (Unity)",
        icon='EXPORT',
    )
    self.layout.operator(
        SHADER_OT_convert_to_unity.bl_idname,
        text="Unity Shader Graphs (.shadergraph)",
        icon='NODE_MATERIAL',
    )
    self.layout.operator(
        SHADER_OT_export_collections_fbx.bl_idname,
        text="Export Collections as FBX (Unity)",
        icon='MESH_DATA',
    )


def register():
    bpy.utils.register_class(SHADER_OT_convert_to_unity)
    bpy.utils.register_class(SHADER_OT_export_collections_fbx)
    bpy.utils.register_class(SHADER_OT_convert_and_export_all)

    # Blender 4.x uses TOPBAR_MT_file_export; older builds use INFO_MT_file_export
    for menu_name in ('TOPBAR_MT_file_export', 'INFO_MT_file_export'):
        menu = getattr(bpy.types, menu_name, None)
        if menu is not None:
            menu.append(export_menu_func)
            break

    print("  All operators registered")


def unregister():
    bpy.utils.unregister_class(SHADER_OT_convert_to_unity)
    bpy.utils.unregister_class(SHADER_OT_export_collections_fbx)
    bpy.utils.unregister_class(SHADER_OT_convert_and_export_all)

    for menu_name in ('TOPBAR_MT_file_export', 'INFO_MT_file_export'):
        menu = getattr(bpy.types, menu_name, None)
        if menu is not None:
            menu.remove(export_menu_func)
            break

    print("  All operators unregistered")
