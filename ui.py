"""
Blender UI Panels
N-panel sidebar: conversion issues list + export controls
Properties panel: per-node conversion steps
"""

import bpy
import os
from . import parser, utils

# ── Preview Collection for Logo ─────────────────────────────────────────────────

_preview_collections = {}

def _get_preview_collection():
    """Get or create preview collection for addon icons"""
    global _preview_collections
    
    if "addon_previews" in _preview_collections:
        return _preview_collections["addon_previews"]
    
    import bpy.utils.previews
    
    pcoll = bpy.utils.previews.new()
    
    # Get the addon directory
    addon_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    logo_path = os.path.join(addon_dir, "gfx", "PIXELAGENT_small.png")
    
    # Load logo if it exists
    if os.path.exists(logo_path):
        pcoll.load("addon_logo", logo_path, 'IMAGE')
    else:
        # Fallback: try without _small
        logo_path = os.path.join(addon_dir, "gfx", "PIXELAGENT.png")
        if os.path.exists(logo_path):
            pcoll.load("addon_logo", logo_path, 'IMAGE')
    
    _preview_collections["addon_previews"] = pcoll
    return pcoll


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_node_mapping():
    try:
        return utils.load_node_mappings()
    except Exception:
        return {}


def _analyze_shader(blender_data, node_mapping):
    """Lightweight analysis used by both panels"""
    from . import socket_handler

    analysis = {
        'total': len(blender_data['nodes']),
        'direct': 0,
        'decompose': 0,
        'approx': 0,
        'incompatible': [],   # list of dicts {name, type, reason}
        'mismatches': [],     # list of strings
        'success': 0,
    }

    for nd in blender_data['nodes']:
        ntype = nd['blender_type']
        mapping = node_mapping.get(ntype, {})
        strategy = mapping.get('strategy', 'incompatible')

        if strategy == 'direct':
            analysis['direct'] += 1
        elif strategy == 'decompose':
            analysis['decompose'] += 1
        elif strategy in ('approximation', 'blend_mapping', 'normal_mapping',
                          'uv_mapping', 'texture_reference', 'attribute_mapping',
                          'procedural_texture'):
            analysis['approx'] += 1
        else:
            analysis['incompatible'].append({
                'name': nd['name'],
                'type': ntype,
                'reason': mapping.get('description', 'No direct Unity equivalent'),
            })

    for conn in blender_data['connections']:
        ok, method = socket_handler.SocketTypeHandler.check_compatibility(
            conn['from_type'], conn['to_type']
        )
        if not ok:
            analysis['mismatches'].append(
                f"{conn['from_node']} ({conn['from_type']}) → "
                f"{conn['to_node']} ({conn['to_type']})"
            )

    convertible = analysis['direct'] + analysis['decompose'] + analysis['approx']
    if analysis['total']:
        analysis['success'] = int(convertible / analysis['total'] * 100)

    return analysis


# ── N-Panel sidebar (View3D > N > Unity Export) ───────────────────────────────

class SHADER_PT_unity_export(bpy.types.Panel):
    """Main Unity export panel in the 3D Viewport sidebar"""
    bl_label = "Unity Export"
    bl_idname = "SHADER_PT_unity_export"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Unity Export"

    def draw(self, context):
        layout = self.layout
        node_mapping = _get_node_mapping()
        scene = context.scene

        # ── Logo ─────────────────────────────────────────────────────────────
        try:
            pcoll = _get_preview_collection()
            if "addon_logo" in pcoll:
                layout.label(text="", icon_value=pcoll["addon_logo"].icon_id)
                layout.separator()
        except Exception:
            pass  # Logo not available, continue without it

        # ── Shader Type Selection ────────────────────────────────────────────
        box = layout.box()
        box.label(text="Shader Settings", icon='SETTINGS')
        
        row = box.row()
        row.label(text="Shader Type:")
        row = box.row()
        row.prop(scene, "unity_shader_type", text="" )

        layout.separator()

        # ── Scene material summary ───────────────────────────────────
        all_mats = [
            slot.material
            for obj in bpy.data.objects if obj.type == 'MESH'
            for slot in obj.material_slots
            if slot.material and slot.material.use_nodes
        ]
        unique_mats = list({m.name: m for m in all_mats}.values())

        box = layout.box()
        box.label(text="Scene Materials", icon='MATERIAL')
        if not unique_mats:
            box.label(text="No node-based materials found", icon='ERROR')
        else:
            box.label(text=f"{len(unique_mats)} material(s) will be exported")
            for mat in unique_mats:
                row = box.row()
                row.label(text=f"  • {mat.name}", icon='MATERIAL_DATA')

        layout.separator()

        # ── Collections summary ──────────────────────────────────────
        collections = list(bpy.context.scene.collection.children)
        box2 = layout.box()
        box2.label(text="Collections (→ FBX)", icon='OUTLINER_COLLECTION')
        if not collections:
            box2.label(text="No top-level collections", icon='INFO')
        else:
            for col in collections:
                mesh_count = sum(1 for o in col.all_objects if o.type == 'MESH')
                row = box2.row()
                row.label(text=f"  • {col.name}  ({mesh_count} mesh(es))", icon='GROUP')

        layout.separator()

        # ── Issues (active material) ─────────────────────────────────
        mat = context.active_object.active_material if (
            context.active_object and context.active_object.type == 'MESH'
        ) else None

        if mat and mat.use_nodes:
            try:
                p = parser.BlenderShaderParser(mat)
                data = p.parse()
                analysis = _analyze_shader(data, node_mapping)

                box3 = layout.box()
                # Header row with success %
                row = box3.row()
                row.label(text=f"Active: {mat.name}", icon='SHADING_RENDERED')
                pct = analysis['success']
                icon = 'CHECKMARK' if pct == 100 else ('INFO' if pct >= 70 else 'ERROR')
                row.label(text=f"{pct}%", icon=icon)

                # Counts
                grid = box3.grid_flow(row_major=True, columns=2, even_columns=True)
                grid.label(text=f"✓ Direct: {analysis['direct']}")
                grid.label(text=f"⊕ Decompose: {analysis['decompose']}")
                grid.label(text=f"≈ Approx: {analysis['approx']}")
                grid.label(text=f"✗ Incompatible: {len(analysis['incompatible'])}")

                # Incompatible nodes
                if analysis['incompatible']:
                    box3.separator()
                    box3.label(text="Incompatible nodes:", icon='ERROR')
                    for item in analysis['incompatible']:
                        row = box3.row()
                        row.alert = True
                        row.label(text=f"  {item['name']}  ({item['type']})")

                # Type mismatches
                if analysis['mismatches']:
                    box3.separator()
                    box3.label(text="Type mismatches:", icon='DRIVER_TRANSFORM')
                    for m in analysis['mismatches'][:5]:
                        box3.label(text=f"  {m}")
                    if len(analysis['mismatches']) > 5:
                        box3.label(text=f"  … and {len(analysis['mismatches']) - 5} more")

            except Exception as e:
                layout.label(text=f"Analysis error: {e}", icon='ERROR')

        layout.separator()

        # ── Export buttons ───────────────────────────────────────────
        col = layout.column(align=True)
        col.scale_y = 1.4

        col.operator("shader.convert_and_export_all",
                     text="⬆  Export All to Unity",
                     icon='EXPORT')
        col.separator()
        col.operator("shader.convert_to_unity",
                     text="Export Shaders Only",
                     icon='NODE_MATERIAL')
        col.operator("shader.export_collections_fbx",
                     text="Export Models Only (FBX)",
                     icon='MESH_DATA')


# ── Properties panel (Material context) ──────────────────────────────────────

class SHADER_PT_conversion_analysis(bpy.types.Panel):
    """Per-material conversion details in the Material Properties panel"""
    bl_label = "Unity Conversion Details"
    bl_idname = "SHADER_PT_conversion_analysis"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.material and context.material.use_nodes

    def draw(self, context):
        layout = self.layout
        material = context.material
        node_mapping = _get_node_mapping()

        try:
            p = parser.BlenderShaderParser(material)
            blender_data = p.parse()
        except Exception as e:
            layout.label(text=f"Parse error: {e}", icon='ERROR')
            return

        analysis = _analyze_shader(blender_data, node_mapping)

        # Summary bar
        box = layout.box()
        row = box.row()
        row.label(text="Conversion success:")
        pct = analysis['success']
        row.label(
            text=f"{pct}%",
            icon='CHECKMARK' if pct == 100 else ('INFO' if pct >= 70 else 'ERROR')
        )

        grid = box.grid_flow(row_major=True, columns=2, even_columns=True)
        grid.label(text=f"✓ Direct: {analysis['direct']}")
        grid.label(text=f"⊕ Decompose: {analysis['decompose']}")
        grid.label(text=f"≈ Approx: {analysis['approx']}")
        grid.label(text=f"✗ Incompatible: {len(analysis['incompatible'])}")

        # Per-node conversion steps from JSON
        layout.separator()
        layout.label(text="Node Conversion Steps", icon='NODETREE')

        has_steps = False
        for nd in blender_data['nodes']:
            ntype = nd['blender_type']
            mapping = node_mapping.get(ntype, {})
            chain = mapping.get('unity_chain')
            if not chain or not chain.get('steps'):
                continue
            has_steps = True

            box = layout.box()
            row = box.row()
            compat = mapping.get('compatibility', '?')
            icon = 'CHECKMARK' if compat == '100%' else ('INFO' if compat >= '90%' else 'ERROR')
            row.label(text=nd['name'], icon='NODE')
            row.label(text=f"→ {mapping.get('unity_name', ntype)}  [{compat}]", icon=icon)

            desc = chain.get('description', '')
            if desc:
                box.label(text=desc)

            steps = chain.get('steps', [])
            for i, step in enumerate(steps[:5]):
                r = box.row()
                r.label(text=f"  {i+1}. {step.get('action', '')}", icon='DOT')
                detail = step.get('node') or step.get('note') or (
                    f"{step.get('from', '')} → {step.get('to', '')}" if step.get('from') else ''
                )
                if detail:
                    r.label(text=detail)
            if len(steps) > 5:
                box.label(text=f"  … and {len(steps) - 5} more steps")

            note = chain.get('blender_conversion_notes', '')
            if note:
                box.label(text=f"💡 {note}", icon='INFO')

        if not has_steps:
            layout.label(text="No detailed steps needed for this material", icon='INFO')

        layout.separator()
        row = layout.row()
        row.scale_y = 1.4
        row.operator("shader.convert_to_unity", text="Export to Unity", icon='EXPORT')


# ── Registration ──────────────────────────────────────────────────────────────

_classes = (
    SHADER_PT_unity_export,
    SHADER_PT_conversion_analysis,
)


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)
    print("  ✓ UI panels registered")


def unregister():
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
    
    # Clean up preview collection
    global _preview_collections
    if "addon_previews" in _preview_collections:
        bpy.utils.previews.remove(_preview_collections["addon_previews"])
        del _preview_collections["addon_previews"]
    
    print("  ✓ UI panels unregistered")
