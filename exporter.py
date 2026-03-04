"""
Unity Exporter
Exports converted shader and FBX to Unity project structure
"""

import json
import os
from pathlib import Path

class UnityExporter:
    """Export converted shader and FBX to Unity project structure"""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.material_folder = self.output_dir / "Materials"
        self.shader_folder = self.output_dir / "Shaders"
        self.model_folder = self.output_dir / "Models"
        self.texture_folder = self.output_dir / "Textures"

    def setup_folders(self):
        """Create folder structure"""
        for folder in [self.material_folder, self.shader_folder, self.model_folder, self.texture_folder]:
            folder.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created folder structure at {self.output_dir}")

    def export_shader_graph(self, unity_graph, name: str):
        """Export Unity shader graph to .shadergraph file"""
        # Sanitize the name to remove dots and extensions
        safe_name = self._sanitize_name(name)
        shader_path = self.shader_folder / f"{safe_name}.shadergraph"
        
        content = {
            'fileID': 11500000,
            'guid': unity_graph.guid,
            'ScriptClass': 'ShaderGraph',
            'exposedProperties': [],
            'fixedSlotCount': -1,
            'nodes': [node.to_dict() for node in unity_graph.nodes.values()],
            'groups': [],
            'pinnedNodes': [],
            'activeTargets': 0,
            'targetData': [],
            'conversion_chains': unity_graph.conversion_chains  # Include conversion steps
        }
        
        with open(shader_path, 'w') as f:
            json.dump(content, f, indent=2)
        
        print(f"✓ Exported shader graph: {shader_path}")
        return shader_path

    def export_material(self, shader_name: str, material_name: str):
        """Export Unity material file"""
        # Sanitize names
        safe_shader_name = self._sanitize_name(shader_name)
        safe_material_name = self._sanitize_name(material_name)
        
        mat_path = self.material_folder / f"{safe_material_name}.mat"
        
        content = f"""%YAML 1.1
%TAG ! tag:yaml.org,2002:
---
!u!21 &2100000
Material:
  serializedVersion: 8
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_Name: {safe_material_name}
  m_Shader: {{fileID: 4800000, guid: {self._generate_guid()}, type: 3}}
  m_ShaderKeywords: 
  m_LightmapFlags: 4
  m_EnableInstancingVariants: 0
  m_DoubleSidedGI: 0
  m_CustomRenderQueue: -1
  stringTagMap: {{}}
  disabledShaderPasses: []
  m_SavedProperties:
    serializedVersion: 3
    m_TexEnvs: []
    m_Floats: []
    m_Colors: []
  m_BuildTextureStacks: []
"""
        
        with open(mat_path, 'w') as f:
            f.write(content)
        
        print(f"✓ Exported material: {mat_path}")
        return mat_path

    def export_fbx_with_material(self, blender_object, material_name: str):
        """Export FBX with material assignment"""
        import bpy
        
        # Sanitize the name
        safe_name = self._sanitize_name(blender_object.name)
        fbx_path = self.model_folder / f"{safe_name}.fbx"
        
        # Select and export
        bpy.context.view_layer.objects.active = blender_object
        blender_object.select_set(True)
        
        bpy.ops.export_scene.fbx(
            filepath=str(fbx_path),
            use_selection=True,
            object_types={'MESH'},
            use_mesh_modifiers=True,
            mesh_smooth_type='OFF',
            use_triangles=True,
            use_custom_properties=True,
            add_leaf_bones=False,
        )
        
        blender_object.select_set(False)
        print(f"✓ Exported FBX model: {fbx_path}")
        return fbx_path

    def export_fbx_from_collection(self, collection_name: str, export_path: str):
        """Export a collection as FBX (wrapper for game_exporter functionality)"""
        import bpy
        
        collection = bpy.data.collections.get(collection_name)
        if not collection:
            print(f"⚠ Collection '{collection_name}' not found")
            return None
        
        # Sanitize the name
        safe_name = self._sanitize_name(collection_name)
        fbx_path = Path(export_path) / f"{safe_name}.fbx"
        
        # Duplicate objects and reset transform
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
            print(f"⚠ No exportable objects in collection '{collection_name}'")
            return None
        
        # Create temporary collection
        temp_collection = bpy.data.collections.new(name=f"Temp_{collection.name}")
        bpy.context.scene.collection.children.link(temp_collection)
        for obj in duplicated_objects:
            temp_collection.objects.link(obj)
        
        # Export FBX
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
        
        # Cleanup
        for obj in duplicated_objects:
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(temp_collection)
        
        print(f"✓ Exported collection as FBX: {fbx_path}")
        return fbx_path

    def export_conversion_readme(self, analysis_data: dict):
        """Export a README.md file with conversion notes when conversion isn't 100%"""
        # Check if there's any incomplete conversion
        has_warnings = False
        warnings = []
        
        if analysis_data.get('incompatible_nodes'):
            has_warnings = True
            warnings.append(f"### Incompatible Nodes ({len(analysis_data['incompatible_nodes'])})\n")
            for node in analysis_data['incompatible_nodes']:
                warnings.append(f"- **{node['name']}** ({node['type']}): {node.get('reason', 'No direct Unity equivalent')}")
            warnings.append("")
        
        if analysis_data.get('approximation_nodes', 0) > 0:
            has_warnings = True
            warnings.append(f"### Approximated Nodes ({analysis_data['approximation_nodes']})\n")
            warnings.append("The following nodes were approximated and may require manual adjustment:")
            if analysis_data.get('approximation_details'):
                for detail in analysis_data['approximation_details']:
                    warnings.append(f"- {detail}")
            warnings.append("")
        
        if analysis_data.get('type_mismatches'):
            has_warnings = True
            warnings.append(f"### Type Mismatches ({len(analysis_data['type_mismatches'])})\n")
            warnings.append("The following socket connections required type conversion:")
            for mismatch in analysis_data['type_mismatches']:
                warnings.append(f"- {mismatch['from']} → {mismatch['to']}")
            warnings.append("")
        
        if analysis_data.get('conversion_notes'):
            has_warnings = True
            warnings.append("### Conversion Notes\n")
            for note in analysis_data['conversion_notes']:
                warnings.append(f"- {note}")
            warnings.append("")
        
        if not has_warnings:
            # 100% conversion - no README needed
            return None
        
        # Generate README content
        readme_content = f"""# Shader Conversion Report

**Original Material:** {analysis_data.get('material_name', 'Unknown')}
**Conversion Rate:** {analysis_data.get('success_rate', 0)}%
**Date:** {self._get_timestamp()}

---

## Summary

This shader was converted from Blender to Unity Shader Graph with the following success rate:
- **Direct Conversion:** {analysis_data.get('direct_nodes', 0)} nodes
- **Decomposed Conversion:** {analysis_data.get('decompose_nodes', 0)} nodes  
- **Approximated Conversion:** {analysis_data.get('approximation_nodes', 0)} nodes
- **Incompatible Nodes:** {len(analysis_data.get('incompatible_nodes', []))} nodes

---

## Issues & Manual Steps Required

"""
        readme_content += "\n".join(warnings)
        
        readme_content += """

---

## Manual Steps Required

1. **Review Incompatible Nodes**: Open the Unity Shader Graph and manually recreate any incompatible nodes using equivalent Unity nodes.

2. **Check Approximated Nodes**: Some nodes were approximated. Verify the visual output and adjust node settings as needed.

3. **Type Mismatches**: If there were type mismatches, you may need to add type conversion nodes (like To Float, To Vector3, etc.) in Unity.

4. **Texture References**: Note any texture references that need to be reassigned in Unity.

---

## Exported Files

- **Shaders**: `.shadergraph` files in the `Shaders/` folder
- **Materials**: `.mat` files in the `Materials/` folder  
- **Models**: `.fbx` files in the `Models/` folder
- **Textures**: Place texture files in the `Textures/` folder and reassign in Unity

---

## Tips for Better Conversion Results

1. Use only Blender nodes that have direct Unity equivalents
2. Avoid complex custom node setups
3. Keep shader graphs simple for best compatibility
4. Use PBR Principled BSDF as the base for best results

---

*Generated by Blender to Unity Shader Converter*
"""
        
        # Write README
        readme_path = self.output_dir / "CONVERSION_README.md"
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        print(f"✓ Exported conversion README: {readme_path}")
        return readme_path

    @staticmethod
    def _sanitize_name(name):
        """Remove dots and extensions from name to make folder/file names safe"""
        # Convert to string if Path
        name = str(name)
        # Remove file extension if present
        name = os.path.splitext(name)[0]
        # Replace dots with underscores
        name = name.replace('.', '_')
        # Replace any other problematic characters
        name = name.replace('\\', '_').replace('/', '_').replace(':', '_')
        name = name.replace('*', '_').replace('?', '_').replace('"', '_')
        name = name.replace('<', '_').replace('>', '_').replace('|', '_')
        # Replace spaces with underscores
        name = name.replace(' ', '_')
        return name

    @staticmethod
    def _generate_guid() -> str:
        """Generate random GUID-like string"""
        import random
        return ''.join(random.choices('0123456789abcdef', k=32))
    
    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
