"""
Blender Operator Definition
Handles the "Convert to Unity" operator in the UI and collection FBX export
"""

import bpy
import os
from pathlib import Path
from . import parser, converter, exporter, utils

# Load node mappings from JSON at addon startup
NODE_MAPPING = utils.load_node_mappings()


class SHADER_OT_convert_to_unity(bpy.types.Operator):
    """Convert selected object's shader to Unity shader graph"""
    bl_idname = "shader.convert_to_unity"
    bl_label = "Convert to Unity"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(
        name="Output Directory",
        description="Directory to export converted shader",
        subtype='DIR_PATH'
    )

    def execute(self, context):
        """Execute the operator"""
        obj = context.active_object
        
        # Validate object and material
        if not obj or not obj.data.materials:
            self.report({'ERROR'}, "No material found on active object")
            return {'CANCELLED'}

        material = obj.data.materials[0]
        if not material.use_nodes:
            self.report({'ERROR'}, "Material does not use shader nodes")
            return {'CANCELLED'}

        try:
            # Parse Blender shader
            print(f"\n📊 Parsing shader: {material.name}")
            parser_instance = parser.BlenderShaderParser(material)
            blender_data = parser_instance.parse()
            print(f"   Nodes: {len(blender_data['nodes'])}")
            print(f"   Connections: {len(blender_data['connections'])}\n")

            # Convert to Unity
            print("🔄 Converting to Unity...")
            converter_instance = converter.ShaderGraphConverter(blender_data, NODE_MAPPING)
            unity_graph = converter_instance.convert()
            
            # Export
            print("💾 Exporting assets...")
            export_instance = exporter.UnityExporter(self.filepath)
            export_instance.setup_folders()
            export_instance.export_shader_graph(unity_graph, material.name)
            export_instance.export_material(material.name, material.name + "_Material")
            export_instance.export_fbx_with_material(obj, material.name)
            
            # Analyze conversion and export README if not 100%
            analysis_data = self._analyze_conversion(blender_data)
            readme_path = export_instance.export_conversion_readme(analysis_data)

            print(f"\n✅ Conversion complete!\n")
            if readme_path:
                self.report({'INFO'}, f"Shader converted to {self.filepath} (see README for notes)")
            else:
                self.report({'INFO'}, f"Shader converted to {self.filepath}")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Conversion failed: {str(e)}")
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}

    def _analyze_conversion(self, blender_data):
        """Analyze the conversion and return data for README"""
        from . import socket_handler
        
        analysis = {
            'material_name': '',
            'total_nodes': len(blender_data['nodes']),
            'direct_nodes': 0,
            'decompose_nodes': 0,
            'approximation_nodes': 0,
            'incompatible_nodes': [],
            'type_mismatches': [],
            'conversion_notes': [],
            'approximation_details': [],
            'success_rate': 0
        }
        
        # Analyze each node
        for node_data in blender_data['nodes']:
            node_type = node_data['blender_type']
            node_mapping_data = NODE_MAPPING.get(node_type, {})
            strategy = node_mapping_data.get('strategy', 'incompatible')
            
            if strategy == 'direct':
                analysis['direct_nodes'] += 1
            elif strategy == 'decompose':
                analysis['decompose_nodes'] += 1
            elif strategy in ['approximation', 'blend_mapping', 'normal_mapping', 'uv_mapping', 'texture_reference']:
                analysis['approximation_nodes'] += 1
                # Add approximation detail
                unity_name = node_mapping_data.get('unity_name', 'Unknown')
                analysis['approximation_details'].append(
                    f"{node_data['name']} ({node_type}) → {unity_name}"
                )
            else:
                analysis['incompatible_nodes'].append({
                    'name': node_data['name'],
                    'type': node_type,
                    'reason': node_mapping_data.get('description', 'No direct Unity equivalent')
                })
                analysis['conversion_notes'].append(
                    f"{node_data['name']} ({node_type}) - No direct Unity equivalent"
                )
        
        # Analyze connections for type mismatches
        for conn in blender_data['connections']:
            is_compat, method = socket_handler.SocketTypeHandler.check_compatibility(
                conn['from_type'], conn['to_type']
            )
            if not is_compat:
                analysis['type_mismatches'].append({
                    'from': f"{conn['from_node']}.{conn['from_socket']} ({conn['from_type']})",
                    'to': f"{conn['to_node']}.{conn['to_socket']} ({conn['to_type']})"
                })
                analysis['conversion_notes'].append(
                    f"Type mismatch: {conn['from_type']} → {conn['to_type']} (added converter)"
                )
        
        # Calculate success rate
        convertible = analysis['direct_nodes'] + analysis['decompose_nodes'] + analysis['approximation_nodes']
        if analysis['total_nodes'] > 0:
            analysis['success_rate'] = int((convertible / analysis['total_nodes']) * 100)
        
        return analysis

    def invoke(self, context, event):
        """Open file browser to select directory"""
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class SHADER_OT_export_collections_fbx(bpy.types.Operator):
    """Export each collection as a separate FBX with zeroed X/Y coordinates"""
    bl_idname = "shader.export_collections_fbx"
    bl_label = "Export Collections as FBX"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(
        name="Output Directory",
        description="Directory to export FBX files",
        subtype='DIR_PATH'
    )

    def execute(self, context):
        """Execute the operator"""
        export_dir = self.filepath
        
        if not export_dir:
            # Use the directory of the current blend file
            export_dir = os.path.dirname(bpy.data.filepath)
            if not export_dir:
                self.report({'ERROR'}, "Please save the Blender file first or specify an output directory.")
                return {'CANCELLED'}
        
        scene = bpy.context.scene
        top_level_collections = scene.collection.children
        
        if not top_level_collections:
            self.report({'WARNING'}, "No top-level collections found to export.")
            return {'CANCELLED'}
        
        exported_count = 0
        for collection in top_level_collections:
            success = self._export_collection_as_fbx(collection, export_dir)
            if success:
                exported_count += 1
        
        self.report({'INFO'}, f"Exported {exported_count} collections as FBX.")
        return {'FINISHED'}

    def _export_collection_as_fbx(self, collection, export_dir):
        """Export a single collection as FBX"""
        bpy.ops.object.select_all(action='DESELECT')

        duplicated_objects = []
        for obj in collection.all_objects:
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
            return False

        # Create a temporary collection
        temp_collection = bpy.data.collections.new(name=f"Temp_{collection.name}")
        bpy.context.scene.collection.children.link(temp_collection)
        for obj in duplicated_objects:
            temp_collection.objects.link(obj)

        # Sanitize collection name - remove dots and extensions
        safe_name = self._sanitize_name(collection.name)
        
        # Export FBX
        fbx_filename = os.path.join(export_dir, f"{safe_name}.fbx")
        bpy.ops.object.select_all(action='DESELECT')
        for obj in duplicated_objects:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = duplicated_objects[0]

        bpy.ops.export_scene.fbx(
            filepath=fbx_filename,
            use_selection=True,
            apply_unit_scale=True,
            apply_scale_options='FBX_SCALE_ALL',
            object_types={'MESH', 'ARMATURE', 'EMPTY'},
            bake_space_transform=True,
            mesh_smooth_type='OFF',
            add_leaf_bones=False,
            use_custom_properties=True,
            axis_forward='-Z',
            axis_up='Y',
        )

        # Cleanup
        for obj in duplicated_objects:
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(temp_collection)
        
        print(f"✓ Exported FBX: {fbx_filename}")
        return True

    @staticmethod
    def _sanitize_name(name):
        """Remove dots and extensions from name to make folder/file names safe"""
        # Remove file extension if present
        name = os.path.splitext(name)[0]
        # Replace dots with underscores
        name = name.replace('.', '_')
        # Replace any other problematic characters
        name = name.replace('\\', '_').replace('/', '_').replace(':', '_')
        name = name.replace('*', '_').replace('?', '_').replace('"', '_')
        name = name.replace('<', '_').replace('>', '_').replace('|', '_')
        return name

    def invoke(self, context, event):
        """Open file browser to select directory"""
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class SHADER_OT_convert_and_export_all(bpy.types.Operator):
    """Convert shader and export collections as FBX in one operation"""
    bl_idname = "shader.convert_and_export_all"
    bl_label = "Convert & Export All (Unity)"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(
        name="Output Directory",
        description="Directory to export converted shader and FBX files",
        subtype='DIR_PATH'
    )

    def execute(self, context):
        """Execute the operator - convert shader and export collections"""
        export_dir = self.filepath
        
        if not export_dir:
            # Use the directory of the current blend file
            export_dir = os.path.dirname(bpy.data.filepath)
            if not export_dir:
                self.report({'ERROR'}, "Please save the Blender file first or specify an output directory.")
                return {'CANCELLED'}
        
        # Sanitize the output folder name to remove dots and extensions
        safe_folder_name = self._sanitize_name(os.path.basename(bpy.data.filepath) or "Exported")
        
        # Create a subfolder for this export
        export_path = os.path.join(export_dir, safe_folder_name)
        
        try:
            # Step 1: Export collections as FBX
            scene = bpy.context.scene
            top_level_collections = scene.collection.children
            
            fbx_exported_count = 0
            if top_level_collections:
                # Create Models folder
                models_folder = os.path.join(export_path, "Models")
                os.makedirs(models_folder, exist_ok=True)
                
                for collection in top_level_collections:
                    success = self._export_collection_as_fbx(collection, models_folder)
                    if success:
                        fbx_exported_count += 1
            
            # Step 2: Convert and export shader if there's an active object with material
            shader_exported = False
            readme_exported = False
            obj = context.active_object
            if obj and obj.data.materials:
                material = obj.data.materials[0]
                if material and material.use_nodes:
                    # Create shader folders
                    shader_folder = os.path.join(export_path, "Shaders")
                    material_folder = os.path.join(export_path, "Materials")
                    texture_folder = os.path.join(export_path, "Textures")
                    os.makedirs(shader_folder, exist_ok=True)
                    os.makedirs(material_folder, exist_ok=True)
                    os.makedirs(texture_folder, exist_ok=True)
                    
                    # Parse and convert shader
                    parser_instance = parser.BlenderShaderParser(material)
                    blender_data = parser_instance.parse()
                    
                    converter_instance = converter.ShaderGraphConverter(blender_data, NODE_MAPPING)
                    unity_graph = converter_instance.convert()
                    
                    # Export shader and material
                    export_instance = exporter.UnityExporter(export_path)
                    export_instance.shader_folder = Path(shader_folder)
                    export_instance.material_folder = Path(material_folder)
                    export_instance.texture_folder = Path(texture_folder)
                    
                    safe_material_name = self._sanitize_name(material.name)
                    export_instance.export_shader_graph(unity_graph, safe_material_name)
                    export_instance.export_material(safe_material_name, safe_material_name + "_Material")
                    
                    # Analyze conversion and export README if not 100%
                    analysis_data = self._analyze_conversion(blender_data)
                    analysis_data['material_name'] = material.name
                    readme_path = export_instance.export_conversion_readme(analysis_data)
                    
                    shader_exported = True
                    readme_exported = readme_path is not None
            
            # Report results
            msg_parts = []
            if fbx_exported_count > 0:
                msg_parts.append(f"{fbx_exported_count} FBX files")
            if shader_exported:
                if readme_exported:
                    msg_parts.append("shader graph (see README for notes)")
                else:
                    msg_parts.append("shader graph")
            
            if msg_parts:
                self.report({'INFO'}, f"Export complete: {', '.join(msg_parts)}")
            else:
                self.report({'WARNING'}, "Nothing to export")
            
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Export failed: {str(e)}")
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}

    def _analyze_conversion(self, blender_data):
        """Analyze the conversion and return data for README"""
        from . import socket_handler
        
        analysis = {
            'material_name': '',
            'total_nodes': len(blender_data['nodes']),
            'direct_nodes': 0,
            'decompose_nodes': 0,
            'approximation_nodes': 0,
            'incompatible_nodes': [],
            'type_mismatches': [],
            'conversion_notes': [],
            'approximation_details': [],
            'success_rate': 0
        }
        
        # Analyze each node
        for node_data in blender_data['nodes']:
            node_type = node_data['blender_type']
            node_mapping_data = NODE_MAPPING.get(node_type, {})
            strategy = node_mapping_data.get('strategy', 'incompatible')
            
            if strategy == 'direct':
                analysis['direct_nodes'] += 1
            elif strategy == 'decompose':
                analysis['decompose_nodes'] += 1
            elif strategy in ['approximation', 'blend_mapping', 'normal_mapping', 'uv_mapping', 'texture_reference']:
                analysis['approximation_nodes'] += 1
                unity_name = node_mapping_data.get('unity_name', 'Unknown')
                analysis['approximation_details'].append(
                    f"{node_data['name']} ({node_type}) → {unity_name}"
                )
            else:
                analysis['incompatible_nodes'].append({
                    'name': node_data['name'],
                    'type': node_type,
                    'reason': node_mapping_data.get('description', 'No direct Unity equivalent')
                })
                analysis['conversion_notes'].append(
                    f"{node_data['name']} ({node_type}) - No direct Unity equivalent"
                )
        
        # Analyze connections for type mismatches
        for conn in blender_data['connections']:
            is_compat, method = socket_handler.SocketTypeHandler.check_compatibility(
                conn['from_type'], conn['to_type']
            )
            if not is_compat:
                analysis['type_mismatches'].append({
                    'from': f"{conn['from_node']}.{conn['from_socket']} ({conn['from_type']})",
                    'to': f"{conn['to_node']}.{conn['to_socket']} ({conn['to_type']})"
                })
                analysis['conversion_notes'].append(
                    f"Type mismatch: {conn['from_type']} → {conn['to_type']} (added converter)"
                )
        
        # Calculate success rate
        convertible = analysis['direct_nodes'] + analysis['decompose_nodes'] + analysis['approximation_nodes']
        if analysis['total_nodes'] > 0:
            analysis['success_rate'] = int((convertible / analysis['total_nodes']) * 100)
        
        return analysis

    def _export_collection_as_fbx(self, collection, export_dir):
        """Export a single collection as FBX"""
        bpy.ops.object.select_all(action='DESELECT')

        duplicated_objects = []
        for obj in collection.all_objects:
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
            return False

        # Create a temporary collection
        temp_collection = bpy.data.collections.new(name=f"Temp_{collection.name}")
        bpy.context.scene.collection.children.link(temp_collection)
        for obj in duplicated_objects:
            temp_collection.objects.link(obj)

        # Sanitize collection name
        safe_name = self._sanitize_name(collection.name)
        
        # Export FBX
        fbx_filename = os.path.join(export_dir, f"{safe_name}.fbx")
        bpy.ops.object.select_all(action='DESELECT')
        for obj in duplicated_objects:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = duplicated_objects[0]

        bpy.ops.export_scene.fbx(
            filepath=fbx_filename,
            use_selection=True,
            apply_unit_scale=True,
            apply_scale_options='FBX_SCALE_ALL',
            object_types={'MESH', 'ARMATURE', 'EMPTY'},
            bake_space_transform=True,
            mesh_smooth_type='OFF',
            add_leaf_bones=False,
            use_custom_properties=True,
            axis_forward='-Z',
            axis_up='Y',
        )

        # Cleanup
        for obj in duplicated_objects:
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(temp_collection)
        
        print(f"✓ Exported FBX: {fbx_filename}")
        return True

    @staticmethod
    def _sanitize_name(name):
        """Remove dots and extensions from name to make folder/file names safe"""
        # Remove file extension if present
        name = os.path.splitext(name)[0]
        # Replace dots with underscores
        name = name.replace('.', '_')
        # Replace any other problematic characters
        name = name.replace('\\', '_').replace('/', '_').replace(':', '_')
        name = name.replace('*', '_').replace('?', '_').replace('"', '_')
        name = name.replace('<', '_').replace('>', '_').replace('|', '_')
        return name

    def invoke(self, context, event):
        """Open file browser to select directory"""
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


def menu_func(self, context):
    """Add operator to Object menu"""
    self.layout.operator(SHADER_OT_convert_to_unity.bl_idname)
    self.layout.separator()
    self.layout.operator(SHADER_OT_export_collections_fbx.bl_idname)
    self.layout.operator(SHADER_OT_convert_and_export_all.bl_idname)


def export_menu_func(self, context):
    """Add operator to File > Export menu"""
    self.layout.separator()
    self.layout.operator(SHADER_OT_convert_to_unity.bl_idname, text="Unity Shader Graph (.shadergraph)")
    self.layout.operator(SHADER_OT_export_collections_fbx.bl_idname, text="Export Collections as FBX (Unity)")
    self.layout.operator(SHADER_OT_convert_and_export_all.bl_idname, text="Convert & Export All (Unity)")


def register():
    """Register operator and menus"""
    bpy.utils.register_class(SHADER_OT_convert_to_unity)
    bpy.utils.register_class(SHADER_OT_export_collections_fbx)
    bpy.utils.register_class(SHADER_OT_convert_and_export_all)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    
    # Blender 4.0+ uses TOPBAR_MT_file_export instead of INFO_MT_file_export
    try:
        bpy.types.INFO_MT_file_export.append(export_menu_func)
    except AttributeError:
        try:
            bpy.types.TOPBAR_MT_file_export.append(export_menu_func)
        except AttributeError:
            # Fallback: add to File menu
            bpy.types.TOPBAR_MT_file.append(export_menu_func)
    
    print("  ✓ All operators registered")


def unregister():
    """Unregister operator and menus"""
    bpy.utils.unregister_class(SHADER_OT_convert_to_unity)
    bpy.utils.unregister_class(SHADER_OT_export_collections_fbx)
    bpy.utils.unregister_class(SHADER_OT_convert_and_export_all)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    
    try:
        bpy.types.INFO_MT_file_export.remove(export_menu_func)
    except AttributeError:
        try:
            bpy.types.TOPBAR_MT_file_export.remove(export_menu_func)
        except AttributeError:
            try:
                bpy.types.TOPBAR_MT_file.remove(export_menu_func)
            except AttributeError:
                pass
    
    print("  ✓ All operators unregistered")
