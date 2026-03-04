"""
Unity Exporter
Exports converted shader and FBX to Unity project structure
"""

import json
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
        shader_path = self.shader_folder / f"{name}.shadergraph"
        
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
        mat_path = self.material_folder / f"{material_name}.mat"
        
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
  m_Name: {material_name}
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
        
        fbx_path = self.model_folder / f"{blender_object.name}.fbx"
        
        # Select and export
        bpy.context.view_layer.objects.active = blender_object
        blender_object.select_set(True)
        
        bpy.ops.export_scene.fbx(
            filepath=str(fbx_path),
            use_selection=True,
            object_types={'MESH'},
            use_mesh_apply_modifiers=True,
            mesh_smooth_type='OFF',
            use_triangles=True,
            use_custom_properties=False,
            add_leaf_bones=False,
        )
        
        blender_object.select_set(False)
        print(f"✓ Exported FBX model: {fbx_path}")
        return fbx_path

    @staticmethod
    def _generate_guid() -> str:
        """Generate random GUID-like string"""
        import random
        return ''.join(random.choices('0123456789abcdef', k=32))
