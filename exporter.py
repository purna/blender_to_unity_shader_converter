"""
Unity Exporter
Exports converted shader graph and FBX files to Unity project structure.
The .shadergraph JSON now contains fully-populated m_SerializableSlots
with mapped Unity property values.
"""

import json
import os
from pathlib import Path


class UnityExporter:
    """Export converted shader and FBX to Unity project structure."""

    def __init__(self, output_dir: str):
        self.output_dir      = Path(output_dir)
        self.material_folder = self.output_dir / "Materials"
        self.shader_folder   = self.output_dir / "Shaders"
        self.model_folder    = self.output_dir / "Models"
        self.texture_folder  = self.output_dir / "Textures"

    def setup_folders(self):
        for folder in [self.material_folder, self.shader_folder,
                       self.model_folder, self.texture_folder]:
            folder.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created folder structure at {self.output_dir}")

    # ── Shader graph export ───────────────────────────────────────────────────

    def export_shader_graph(self, unity_graph, name: str):
        """Serialise a UnityShaderGraph to a .shadergraph JSON file."""
        safe_name   = self._sanitize_name(name)
        shader_path = self.shader_folder / f"{safe_name}.shadergraph"

        # Build the serialised node list
        serialised_nodes = []
        for node in unity_graph.nodes.values():
            node_dict = {
                'm_ObjectId': node.guid,
                'm_Type':     node.unity_type,
                'm_Group':    {'m_Id': ''},
                'm_Name':     node.unity_name,
                'm_DrawState': {
                    'm_Expanded': True,
                    'm_Position': {'x': 0, 'y': 0, 'width': 0, 'height': 0},
                },
                # Slot references (IDs only – Unity resolves them from m_SerializableSlots)
                'm_Slots': [{'m_Id': s['m_Id']} for s in node.slots],
                # Full slot data including mapped values
                'm_SerializableSlots': node.slots,
            }

            # Attach texture reference if present (for SampleTexture2D nodes)
            bp = getattr(node, 'blender_props', {})
            if bp.get('image_name'):
                node_dict['m_TextureReference'] = {
                    'blender_image':  bp['image_name'],
                    'blender_path':   bp.get('image_path', ''),
                    'colorspace':     bp.get('colorspace', 'sRGB'),
                    'note': (
                        f"Assign texture '{bp['image_name']}' manually in Unity. "
                        "Import the texture into your Assets folder first."
                    ),
                }

            # Attach UV map name if present
            if bp.get('uv_map'):
                node_dict['m_UVMap'] = bp['uv_map']

            # Attach operation name for Math/VectorMath nodes
            if bp.get('operation'):
                node_dict['m_Operation'] = bp['operation']

            # Attach blend mode for Mix nodes
            if bp.get('blend_mode'):
                node_dict['m_BlendType'] = bp['blend_mode']

            serialised_nodes.append(node_dict)

        # Build edge list
        serialised_edges = []
        for edge in unity_graph.edges:
            serialised_edges.append({
                'm_OutputSlot': edge['m_OutputSlot'],
                'm_InputSlot':  edge['m_InputSlot'],
            })

        content = {
            'fileID': 11500000,
            'guid':   unity_graph.guid,
            'ScriptClass': 'ShaderSubGraph' if 'subgraph' in safe_name.lower() else 'ShaderGraph',
            'generationVersion': 1,
            'm_ObjectId': unity_graph.guid,
            'm_ActiveTargets': [],
            'exposedProperties': self._build_exposed_properties(unity_graph),
            'nodes':    serialised_nodes,
            'edges':    serialised_edges,
            'groups':   [],
            'pinnedNodes': [],
            # Human-readable conversion reference (not used by Unity, useful for artists)
            'conversion_chains': unity_graph.conversion_chains,
        }

        with open(shader_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2)

        print(f"✓ Exported shader graph: {shader_path}")
        return shader_path

    def _build_exposed_properties(self, unity_graph) -> list:
        """
        Build the exposedProperties list from texture and float nodes so
        artists can tweak values from the Material Inspector in Unity.
        """
        props = []
        seen  = set()

        for node in unity_graph.nodes.values():
            bp = getattr(node, 'blender_props', {})

            # Expose textures as Texture2D properties
            img = bp.get('image_name')
            if img and img not in seen:
                seen.add(img)
                props.append({
                    'm_ObjectId':    self._generate_guid(),
                    'm_Name':        self._sanitize_name(img),
                    'm_DisplayName': img,
                    'm_Type':        'UnityEditor.ShaderGraph.Texture2DShaderProperty',
                    'm_Value': {
                        'texture': {'instanceID': 0},
                        'modifiableTextureData': {'instanceID': 0},
                    },
                })

        return props

    # ── Material export ───────────────────────────────────────────────────────

    def export_material(self, shader_name: str, material_name: str):
        """Export a Unity .mat file referencing the converted shader graph."""
        safe_shader   = self._sanitize_name(shader_name)
        safe_material = self._sanitize_name(material_name)
        mat_path      = self.material_folder / f"{safe_material}.mat"

        content = (
            f"%YAML 1.1\n"
            f"%TAG ! tag:yaml.org,2002:\n"
            f"---\n"
            f"!u!21 &2100000\n"
            f"Material:\n"
            f"  serializedVersion: 8\n"
            f"  m_ObjectHideFlags: 0\n"
            f"  m_CorrespondingSourceObject: {{fileID: 0}}\n"
            f"  m_PrefabInstance: {{fileID: 0}}\n"
            f"  m_PrefabAsset: {{fileID: 0}}\n"
            f"  m_Name: {safe_material}\n"
            f"  m_Shader: {{fileID: 4800000, guid: {self._generate_guid()}, type: 3}}\n"
            f"  m_ShaderKeywords: \n"
            f"  m_LightmapFlags: 4\n"
            f"  m_EnableInstancingVariants: 0\n"
            f"  m_DoubleSidedGI: 0\n"
            f"  m_CustomRenderQueue: -1\n"
            f"  stringTagMap: {{}}\n"
            f"  disabledShaderPasses: []\n"
            f"  m_SavedProperties:\n"
            f"    serializedVersion: 3\n"
            f"    m_TexEnvs: []\n"
            f"    m_Floats: []\n"
            f"    m_Colors: []\n"
            f"  m_BuildTextureStacks: []\n"
            f"  # ShaderGraph: {safe_shader}.shadergraph\n"
        )

        with open(mat_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✓ Exported material: {mat_path}")
        return mat_path

    # ── FBX exports ───────────────────────────────────────────────────────────

    def export_fbx_with_material(self, blender_object, material_name: str):
        """Export a single mesh object as FBX."""
        import bpy

        safe_name = self._sanitize_name(blender_object.name)
        fbx_path  = self.model_folder / f"{safe_name}.fbx"

        bpy.context.view_layer.objects.active = blender_object
        blender_object.select_set(True)

        bpy.ops.export_scene.fbx(
            filepath=str(fbx_path),
            use_selection=True,
            object_types={'MESH'},
            use_mesh_modifiers=True,
            mesh_smooth_type='OFF',
            use_triangles=True,
            add_leaf_bones=False,
        )

        blender_object.select_set(False)
        print(f"✓ Exported FBX model: {fbx_path}")
        return fbx_path

    def export_fbx_from_collection(self, collection_name: str, export_path: str):
        """Export a named collection as FBX."""
        import bpy

        collection = bpy.data.collections.get(collection_name)
        if not collection:
            print(f"⚠ Collection '{collection_name}' not found")
            return None

        safe_name = self._sanitize_name(collection_name)
        fbx_path  = Path(export_path) / f"{safe_name}.fbx"

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
            print(f"⚠ No exportable objects in collection '{collection_name}'")
            return None

        temp_col = bpy.data.collections.new(name=f"Temp_{collection.name}")
        bpy.context.scene.collection.children.link(temp_col)
        for obj in duplicated_objects:
            temp_col.objects.link(obj)

        bpy.ops.object.select_all(action='DESELECT')
        for obj in duplicated_objects:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = duplicated_objects[0]

        bpy.ops.export_scene.fbx(
            filepath=str(fbx_path),
            use_selection=True,
            apply_unit_scale=True,
            apply_scale_options='FBX_SCALE_ALL',
            object_types={'MESH', 'ARMATURE', 'EMPTY'},
            bake_space_transform=True,
            mesh_smooth_type='OFF',
            add_leaf_bones=False,
            axis_forward='-Z',
            axis_up='Y',
        )

        for obj in duplicated_objects:
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(temp_col)

        print(f"✓ Exported collection as FBX: {fbx_path}")
        return fbx_path

    # ── Conversion README ─────────────────────────────────────────────────────

    def export_conversion_readme(self, analysis_data: dict):
        """Write CONVERSION_README.md when the conversion is not 100%."""
        sections = []

        if analysis_data.get('incompatible_nodes'):
            sections.append(
                f"### Incompatible Nodes ({len(analysis_data['incompatible_nodes'])})\n"
            )
            for node in analysis_data['incompatible_nodes']:
                sections.append(
                    f"- **{node['name']}** ({node['type']}): "
                    f"{node.get('reason', 'No direct Unity equivalent')}"
                )
            sections.append("")

        if analysis_data.get('approximation_nodes', 0) > 0:
            sections.append(
                f"### Approximated Nodes ({analysis_data['approximation_nodes']})\n"
            )
            sections.append(
                "The following nodes were approximated and may need manual adjustment:"
            )
            for detail in analysis_data.get('approximation_details', []):
                sections.append(f"- {detail}")
            sections.append("")

        if analysis_data.get('type_mismatches'):
            sections.append(
                f"### Type Mismatches ({len(analysis_data['type_mismatches'])})\n"
            )
            for mm in analysis_data['type_mismatches']:
                sections.append(f"- {mm['from']} → {mm['to']}")
            sections.append("")

        if analysis_data.get('conversion_notes'):
            sections.append("### Conversion Notes\n")
            for note in analysis_data['conversion_notes']:
                sections.append(f"- {note}")
            sections.append("")

        if not sections:
            return None   # 100 % – no README needed

        readme = (
            f"# Shader Conversion Report\n\n"
            f"**Original Material:** {analysis_data.get('material_name', 'Unknown')}\n"
            f"**Conversion Rate:** {analysis_data.get('success_rate', 0)}%\n"
            f"**Date:** {self._get_timestamp()}\n\n"
            f"---\n\n"
            f"## Summary\n\n"
            f"- **Direct:** {analysis_data.get('direct_nodes', 0)} nodes\n"
            f"- **Decomposed:** {analysis_data.get('decompose_nodes', 0)} nodes\n"
            f"- **Approximated:** {analysis_data.get('approximation_nodes', 0)} nodes\n"
            f"- **Incompatible:** {len(analysis_data.get('incompatible_nodes', []))} nodes\n\n"
            f"---\n\n"
            f"## Issues & Manual Steps Required\n\n"
            + "\n".join(sections)
            + "\n\n---\n\n"
            "## Manual Steps Required\n\n"
            "1. **Incompatible Nodes** – Recreate manually in Unity Shader Graph.\n"
            "2. **Approximated Nodes** – Verify visual output; adjust as needed.\n"
            "3. **Type Mismatches** – Add conversion nodes (To Float, To Vector3, etc.).\n"
            "4. **Textures** – Assign texture assets in the Unity Shader Graph editor.\n\n"
            "---\n\n"
            "## Exported Files\n\n"
            "- `Shaders/` – `.shadergraph` files\n"
            "- `Materials/` – `.mat` files\n"
            "- `Models/` – `.fbx` files\n"
            "- `Textures/` – Place exported textures here and reassign in Unity\n\n"
            "---\n\n"
            "*Generated by Blender to Unity Shader Converter*\n"
        )

        readme_path = self.output_dir / "CONVERSION_README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme)

        print(f"✓ Exported conversion README: {readme_path}")
        return readme_path

    # ── Utilities ─────────────────────────────────────────────────────────────

    @staticmethod
    def _sanitize_name(name: str) -> str:
        name = str(name)
        name = os.path.splitext(name)[0]
        for ch in r'\/:*?"<>|. ':
            name = name.replace(ch, '_')
        return name.strip('_') or "Exported"

    @staticmethod
    def _generate_guid() -> str:
        import random
        return ''.join(random.choices('0123456789abcdef', k=32))

    @staticmethod
    def _get_timestamp() -> str:
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
