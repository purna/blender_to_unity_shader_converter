"""
Unity Exporter
Exports converted shader graph and FBX files to Unity project structure.
The .shadergraph JSON now contains the proper URP multi-object format.
"""

import json
import os
import uuid
from pathlib import Path
from . import fbx_helper


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

    def export_shader_graph(self, unity_graph, name: str, shader_type: str = 'UNIVERSAL'):
        """Export a Unity ShaderGraph in the proper URP multi-object JSON format.
        
        Args:
            unity_graph: The converted UnityShaderGraph object
            name: Name for the shader graph file
            shader_type: One of 'UNIVERSAL' (URP), 'BUILTIN', or 'CUSTOM_RT'
        """
        safe_name   = self._sanitize_name(name)
        shader_path = self.shader_folder / f"{safe_name}.shadergraph"
        
        print(f"[DEBUG] Exporting shader: {name} -> {shader_path}")

        # Generate GUIDs for all required objects
        graph_guid = unity_graph.guid or self._generate_guid()
        
        # Generate GUIDs for block nodes and slots
        vertex_position_block_id = self._generate_guid()
        vertex_normal_block_id = self._generate_guid()
        vertex_tangent_block_id = self._generate_guid()
        fragment_basecolor_block_id = self._generate_guid()
        fragment_normal_block_id = self._generate_guid()
        fragment_metallic_block_id = self._generate_guid()
        fragment_smoothness_block_id = self._generate_guid()
        fragment_emission_block_id = self._generate_guid()
        fragment_occlusion_block_id = self._generate_guid()
        
        # Slot GUIDs
        position_slot_id = self._generate_guid()
        normal_slot_id = self._generate_guid()
        tangent_slot_id = self._generate_guid()
        basecolor_slot_id = self._generate_guid()
        normalts_slot_id = self._generate_guid()
        metallic_slot_id = self._generate_guid()
        smoothness_slot_id = self._generate_guid()
        emission_slot_id = self._generate_guid()
        occlusion_slot_id = self._generate_guid()
        
        # Category and target GUIDs
        category_id = self._generate_guid()
        target_id = self._generate_guid()
        subtarget_id = self._generate_guid()
        
        # Build the list of JSON objects (multi-object format)
        objects = []
        
        # 1. GraphData (main container)
        graph_data = {
            "m_SGVersion": 3,
            "m_Type": "UnityEditor.ShaderGraph.GraphData",
            "m_ObjectId": graph_guid,
            "m_Properties": [],
            "m_Keywords": [],
            "m_Dropdowns": [],
            "m_CategoryData": [{"m_Id": category_id}],
            "m_Nodes": [],  # Will be filled with node references
            "m_GroupDatas": [],
            "m_StickyNoteDatas": [],
            "m_Edges": [],
            "m_VertexContext": {
                "m_Position": {"x": 0.0, "y": 0.0},
                "m_Blocks": [
                    {"m_Id": vertex_position_block_id},
                    {"m_Id": vertex_normal_block_id},
                    {"m_Id": vertex_tangent_block_id}
                ]
            },
            "m_FragmentContext": {
                "m_Position": {"x": 0.0, "y": 200.0},
                "m_Blocks": [
                    {"m_Id": fragment_basecolor_block_id},
                    {"m_Id": fragment_normal_block_id},
                    {"m_Id": fragment_metallic_block_id},
                    {"m_Id": fragment_smoothness_block_id},
                    {"m_Id": fragment_occlusion_block_id},
                    {"m_Id": fragment_emission_block_id}
                ]
            },
            "m_PreviewData": {
                "serializedMesh": {
                    "m_SerializedMesh": "{\"mesh\":{\"instanceID\":0}}",
                    "m_Guid": ""
                },
                "preventRotation": False
            },
            "m_Path": "Shader Graphs",
            "m_GraphPrecision": 1,
            "m_PreviewMode": 2,
            "m_OutputNode": {"m_Id": ""},
            "m_SubDatas": [],
            "m_ActiveTargets": [{"m_Id": target_id}]
        }
        objects.append(graph_data)
        
        # 2. VertexDescription.Position BlockNode
        objects.append({
            "m_SGVersion": 0,
            "m_Type": "UnityEditor.ShaderGraph.BlockNode",
            "m_ObjectId": vertex_position_block_id,
            "m_Group": {"m_Id": ""},
            "m_Name": "VertexDescription.Position",
            "m_DrawState": {
                "m_Expanded": True,
                "m_Position": {"serializedVersion": "2", "x": 0.0, "y": 0.0, "width": 0.0, "height": 0.0}
            },
            "m_Slots": [{"m_Id": position_slot_id}],
            "synonyms": [],
            "m_Precision": 0,
            "m_PreviewExpanded": True,
            "m_DismissedVersion": 0,
            "m_PreviewMode": 0,
            "m_CustomColors": {"m_SerializableColors": []},
            "m_SerializedDescriptor": "VertexDescription.Position"
        })
        
        # 3. Position MaterialSlot
        objects.append({
            "m_SGVersion": 0,
            "m_Type": "UnityEditor.ShaderGraph.PositionMaterialSlot",
            "m_ObjectId": position_slot_id,
            "m_Id": 0,
            "m_DisplayName": "Position",
            "m_SlotType": 0,
            "m_Hidden": False,
            "m_ShaderOutputName": "Position",
            "m_StageCapability": 1,
            "m_Value": {"x": 0.0, "y": 0.0, "z": 0.0},
            "m_DefaultValue": {"x": 0.0, "y": 0.0, "z": 0.0},
            "m_Labels": [],
            "m_Space": 0
        })
        
        # 4. VertexDescription.Normal BlockNode
        objects.append({
            "m_SGVersion": 0,
            "m_Type": "UnityEditor.ShaderGraph.BlockNode",
            "m_ObjectId": vertex_normal_block_id,
            "m_Group": {"m_Id": ""},
            "m_Name": "VertexDescription.Normal",
            "m_DrawState": {
                "m_Expanded": True,
                "m_Position": {"serializedVersion": "2", "x": 0.0, "y": 0.0, "width": 0.0, "height": 0.0}
            },
            "m_Slots": [{"m_Id": normal_slot_id}],
            "synonyms": [],
            "m_Precision": 0,
            "m_PreviewExpanded": True,
            "m_DismissedVersion": 0,
            "m_PreviewMode": 0,
            "m_CustomColors": {"m_SerializableColors": []},
            "m_SerializedDescriptor": "VertexDescription.Normal"
        })
        
        # 5. Normal MaterialSlot (Vertex)
        objects.append({
            "m_SGVersion": 0,
            "m_Type": "UnityEditor.ShaderGraph.NormalMaterialSlot",
            "m_ObjectId": normal_slot_id,
            "m_Id": 0,
            "m_DisplayName": "Normal",
            "m_SlotType": 0,
            "m_Hidden": False,
            "m_ShaderOutputName": "Normal",
            "m_StageCapability": 1,
            "m_Value": {"x": 0.0, "y": 0.0, "z": 0.0},
            "m_DefaultValue": {"x": 0.0, "y": 0.0, "z": 0.0},
            "m_Labels": [],
            "m_Space": 0
        })
        
        # 6. VertexDescription.Tangent BlockNode
        objects.append({
            "m_SGVersion": 0,
            "m_Type": "UnityEditor.ShaderGraph.BlockNode",
            "m_ObjectId": vertex_tangent_block_id,
            "m_Group": {"m_Id": ""},
            "m_Name": "VertexDescription.Tangent",
            "m_DrawState": {
                "m_Expanded": True,
                "m_Position": {"serializedVersion": "2", "x": 0.0, "y": 0.0, "width": 0.0, "height": 0.0}
            },
            "m_Slots": [{"m_Id": tangent_slot_id}],
            "synonyms": [],
            "m_Precision": 0,
            "m_PreviewExpanded": True,
            "m_DismissedVersion": 0,
            "m_PreviewMode": 0,
            "m_CustomColors": {"m_SerializableColors": []},
            "m_SerializedDescriptor": "VertexDescription.Tangent"
        })
        
        # 7. Tangent MaterialSlot
        objects.append({
            "m_SGVersion": 0,
            "m_Type": "UnityEditor.ShaderGraph.TangentMaterialSlot",
            "m_ObjectId": tangent_slot_id,
            "m_Id": 0,
            "m_DisplayName": "Tangent",
            "m_SlotType": 0,
            "m_Hidden": False,
            "m_ShaderOutputName": "Tangent",
            "m_StageCapability": 1,
            "m_Value": {"x": 0.0, "y": 0.0, "z": 0.0},
            "m_DefaultValue": {"x": 0.0, "y": 0.0, "z": 0.0},
            "m_Labels": [],
            "m_Space": 0
        })
        
        # 8. SurfaceDescription.BaseColor BlockNode
        objects.append({
            "m_SGVersion": 0,
            "m_Type": "UnityEditor.ShaderGraph.BlockNode",
            "m_ObjectId": fragment_basecolor_block_id,
            "m_Group": {"m_Id": ""},
            "m_Name": "SurfaceDescription.BaseColor",
            "m_DrawState": {
                "m_Expanded": True,
                "m_Position": {"serializedVersion": "2", "x": 0.0, "y": 0.0, "width": 0.0, "height": 0.0}
            },
            "m_Slots": [{"m_Id": basecolor_slot_id}],
            "synonyms": [],
            "m_Precision": 0,
            "m_PreviewExpanded": True,
            "m_DismissedVersion": 0,
            "m_PreviewMode": 0,
            "m_CustomColors": {"m_SerializableColors": []},
            "m_SerializedDescriptor": "SurfaceDescription.BaseColor"
        })
        
        # 9. BaseColor MaterialSlot
        # Check if we have a color value from the converted graph
        basecolor_value = self._extract_basecolor_value(unity_graph)
        objects.append({
            "m_SGVersion": 0,
            "m_Type": "UnityEditor.ShaderGraph.ColorRGBMaterialSlot",
            "m_ObjectId": basecolor_slot_id,
            "m_Id": 0,
            "m_DisplayName": "Base Color",
            "m_SlotType": 0,
            "m_Hidden": False,
            "m_ShaderOutputName": "BaseColor",
            "m_StageCapability": 2,
            "m_Value": basecolor_value,
            "m_DefaultValue": basecolor_value,
            "m_Labels": [],
            "m_ColorMode": 0,
            "m_DefaultColor": {"r": 0.5, "g": 0.5, "b": 0.5, "a": 1.0}
        })
        
        # 10. SurfaceDescription.NormalTS BlockNode
        objects.append({
            "m_SGVersion": 0,
            "m_Type": "UnityEditor.ShaderGraph.BlockNode",
            "m_ObjectId": fragment_normal_block_id,
            "m_Group": {"m_Id": ""},
            "m_Name": "SurfaceDescription.NormalTS",
            "m_DrawState": {
                "m_Expanded": True,
                "m_Position": {"serializedVersion": "2", "x": 0.0, "y": 0.0, "width": 0.0, "height": 0.0}
            },
            "m_Slots": [{"m_Id": normalts_slot_id}],
            "synonyms": [],
            "m_Precision": 0,
            "m_PreviewExpanded": True,
            "m_DismissedVersion": 0,
            "m_PreviewMode": 0,
            "m_CustomColors": {"m_SerializableColors": []},
            "m_SerializedDescriptor": "SurfaceDescription.NormalTS"
        })
        
        # 11. NormalTS MaterialSlot (Fragment)
        objects.append({
            "m_SGVersion": 0,
            "m_Type": "UnityEditor.ShaderGraph.NormalMaterialSlot",
            "m_ObjectId": normalts_slot_id,
            "m_Id": 0,
            "m_DisplayName": "Normal (Tangent Space)",
            "m_SlotType": 0,
            "m_Hidden": False,
            "m_ShaderOutputName": "NormalTS",
            "m_StageCapability": 2,
            "m_Value": {"x": 0.0, "y": 0.0, "z": 1.0},
            "m_DefaultValue": {"x": 0.0, "y": 0.0, "z": 1.0},
            "m_Labels": [],
            "m_Space": 3
        })
        
        # 12. SurfaceDescription.Metallic BlockNode
        metallic_value = self._extract_metallic_value(unity_graph)
        objects.append({
            "m_SGVersion": 0,
            "m_Type": "UnityEditor.ShaderGraph.BlockNode",
            "m_ObjectId": fragment_metallic_block_id,
            "m_Group": {"m_Id": ""},
            "m_Name": "SurfaceDescription.Metallic",
            "m_DrawState": {
                "m_Expanded": True,
                "m_Position": {"serializedVersion": "2", "x": 0.0, "y": 0.0, "width": 0.0, "height": 0.0}
            },
            "m_Slots": [{"m_Id": metallic_slot_id}],
            "synonyms": [],
            "m_Precision": 0,
            "m_PreviewExpanded": True,
            "m_DismissedVersion": 0,
            "m_PreviewMode": 0,
            "m_CustomColors": {"m_SerializableColors": []},
            "m_SerializedDescriptor": "SurfaceDescription.Metallic"
        })
        
        # 13. Metallic MaterialSlot
        objects.append({
            "m_SGVersion": 0,
            "m_Type": "UnityEditor.ShaderGraph.Vector1MaterialSlot",
            "m_ObjectId": metallic_slot_id,
            "m_Id": 0,
            "m_DisplayName": "Metallic",
            "m_SlotType": 0,
            "m_Hidden": False,
            "m_ShaderOutputName": "Metallic",
            "m_StageCapability": 2,
            "m_Value": metallic_value,
            "m_DefaultValue": metallic_value,
            "m_Labels": [],
            "m_LiteralMode": False
        })
        
        # 14. SurfaceDescription.Smoothness BlockNode
        smoothness_value = self._extract_smoothness_value(unity_graph)
        objects.append({
            "m_SGVersion": 0,
            "m_Type": "UnityEditor.ShaderGraph.BlockNode",
            "m_ObjectId": fragment_smoothness_block_id,
            "m_Group": {"m_Id": ""},
            "m_Name": "SurfaceDescription.Smoothness",
            "m_DrawState": {
                "m_Expanded": True,
                "m_Position": {"serializedVersion": "2", "x": 0.0, "y": 0.0, "width": 0.0, "height": 0.0}
            },
            "m_Slots": [{"m_Id": smoothness_slot_id}],
            "synonyms": [],
            "m_Precision": 0,
            "m_PreviewExpanded": True,
            "m_DismissedVersion": 0,
            "m_PreviewMode": 0,
            "m_CustomColors": {"m_SerializableColors": []},
            "m_SerializedDescriptor": "SurfaceDescription.Smoothness"
        })
        
        # 15. Smoothness MaterialSlot
        objects.append({
            "m_SGVersion": 0,
            "m_Type": "UnityEditor.ShaderGraph.Vector1MaterialSlot",
            "m_ObjectId": smoothness_slot_id,
            "m_Id": 0,
            "m_DisplayName": "Smoothness",
            "m_SlotType": 0,
            "m_Hidden": False,
            "m_ShaderOutputName": "Smoothness",
            "m_StageCapability": 2,
            "m_Value": smoothness_value,
            "m_DefaultValue": smoothness_value,
            "m_Labels": [],
            "m_LiteralMode": False
        })
        
        # 16. SurfaceDescription.Occlusion BlockNode
        objects.append({
            "m_SGVersion": 0,
            "m_Type": "UnityEditor.ShaderGraph.BlockNode",
            "m_ObjectId": fragment_occlusion_block_id,
            "m_Group": {"m_Id": ""},
            "m_Name": "SurfaceDescription.Occlusion",
            "m_DrawState": {
                "m_Expanded": True,
                "m_Position": {"serializedVersion": "2", "x": 0.0, "y": 0.0, "width": 0.0, "height": 0.0}
            },
            "m_Slots": [{"m_Id": occlusion_slot_id}],
            "synonyms": [],
            "m_Precision": 0,
            "m_PreviewExpanded": True,
            "m_DismissedVersion": 0,
            "m_PreviewMode": 0,
            "m_CustomColors": {"m_SerializableColors": []},
            "m_SerializedDescriptor": "SurfaceDescription.Occlusion"
        })
        
        # 17. Occlusion MaterialSlot
        objects.append({
            "m_SGVersion": 0,
            "m_Type": "UnityEditor.ShaderGraph.Vector1MaterialSlot",
            "m_ObjectId": occlusion_slot_id,
            "m_Id": 0,
            "m_DisplayName": "Ambient Occlusion",
            "m_SlotType": 0,
            "m_Hidden": False,
            "m_ShaderOutputName": "Occlusion",
            "m_StageCapability": 2,
            "m_Value": 1.0,
            "m_DefaultValue": 1.0,
            "m_Labels": [],
            "m_LiteralMode": False
        })
        
        # 18. SurfaceDescription.Emission BlockNode
        emission_value = self._extract_emission_value(unity_graph)
        objects.append({
            "m_SGVersion": 0,
            "m_Type": "UnityEditor.ShaderGraph.BlockNode",
            "m_ObjectId": fragment_emission_block_id,
            "m_Group": {"m_Id": ""},
            "m_Name": "SurfaceDescription.Emission",
            "m_DrawState": {
                "m_Expanded": True,
                "m_Position": {"serializedVersion": "2", "x": 0.0, "y": 0.0, "width": 0.0, "height": 0.0}
            },
            "m_Slots": [{"m_Id": emission_slot_id}],
            "synonyms": [],
            "m_Precision": 0,
            "m_PreviewExpanded": True,
            "m_DismissedVersion": 0,
            "m_PreviewMode": 0,
            "m_CustomColors": {"m_SerializableColors": []},
            "m_SerializedDescriptor": "SurfaceDescription.Emission"
        })
        
        # 19. Emission MaterialSlot
        objects.append({
            "m_SGVersion": 0,
            "m_Type": "UnityEditor.ShaderGraph.ColorRGBMaterialSlot",
            "m_ObjectId": emission_slot_id,
            "m_Id": 0,
            "m_DisplayName": "Emission",
            "m_SlotType": 0,
            "m_Hidden": False,
            "m_ShaderOutputName": "Emission",
            "m_StageCapability": 2,
            "m_Value": emission_value,
            "m_DefaultValue": emission_value,
            "m_Labels": [],
            "m_ColorMode": 1,
            "m_DefaultColor": {"r": 0.0, "g": 0.0, "b": 0.0, "a": 1.0}
        })
        
        # 20. CategoryData
        objects.append({
            "m_SGVersion": 0,
            "m_Type": "UnityEditor.ShaderGraph.CategoryData",
            "m_ObjectId": category_id,
            "m_Name": "",
            "m_ChildObjectList": []
        })
        
        # 21. UniversalTarget (URP) or Built-in or Custom RT Target
        if shader_type == 'UNIVERSAL':
            objects.append({
                "m_SGVersion": 1,
                "m_Type": "UnityEditor.Rendering.Universal.ShaderGraph.UniversalTarget",
                "m_ObjectId": target_id,
                "m_Datas": [],
                "m_ActiveSubTarget": {"m_Id": subtarget_id},
                "m_AllowMaterialOverride": False,
                "m_SurfaceType": 0,
                "m_ZTestMode": 4,
                "m_ZWriteControl": 0,
                "m_AlphaMode": 0,
                "m_RenderFace": 2,
                "m_AlphaClip": False,
                "m_CastShadows": True,
                "m_ReceiveShadows": True,
                "m_DisableTint": False,
                "m_Sort3DAs2DCompatible": False,
                "m_AdditionalMotionVectorMode": 0,
                "m_AlembicMotionVectors": False,
                "m_SupportsLODCrossFade": False,
                "m_CustomEditorGUI": "",
                "m_SupportVFX": False
            })
            
            # 22. UniversalLitSubTarget
            objects.append({
                "m_SGVersion": 2,
                "m_Type": "UnityEditor.Rendering.Universal.ShaderGraph.UniversalLitSubTarget",
                "m_ObjectId": subtarget_id,
                "m_WorkflowMode": 1,
                "m_NormalDropOffSpace": 0,
                "m_ClearCoat": False,
                "m_BlendModePreserveSpecular": True
            })
        elif shader_type == 'BUILTIN':
            objects.append({
                "m_SGVersion": 2,
                "m_Type": "UnityEditor.Rendering.BuiltIn.ShaderGraph.BuiltInTarget",
                "m_ObjectId": target_id,
                "m_Datas": [],
                "m_ActiveSubTarget": {"m_Id": subtarget_id},
                "m_AllowMaterialOverride": False,
                "m_SurfaceType": 0,
                "m_ZWriteControl": 0,
                "m_ZTestMode": 4,
                "m_AlphaMode": 0,
                "m_RenderFace": 2,
                "m_AlphaClip": False,
                "m_CustomEditorGUI": ""
            })
            
            # BuiltInLitSubTarget
            objects.append({
                "m_SGVersion": 0,
                "m_Type": "UnityEditor.Rendering.BuiltIn.ShaderGraph.BuiltInLitSubTarget",
                "m_ObjectId": subtarget_id,
                "m_WorkflowMode": 1,
                "m_NormalDropOffSpace": 0
            })
        elif shader_type == 'CUSTOM_RT':
            objects.append({
                "m_SGVersion": 0,
                "m_Type": "UnityEditor.Rendering.CustomRenderTexture.ShaderGraph.CustomRenderTextureTarget",
                "m_ObjectId": target_id,
                "m_ActiveSubTarget": {"m_Id": subtarget_id},
                "m_CustomEditorGUI": ""
            })
            
            # CustomTextureSubTarget
            objects.append({
                "m_SGVersion": 0,
                "m_Type": "UnityEditor.Rendering.CustomRenderTexture.ShaderGraph.CustomTextureSubTarget",
                "m_ObjectId": subtarget_id
            })

        # Write as multi-object JSON (each object on its own line for Unity compatibility)
        with open(shader_path, 'w', encoding='utf-8') as f:
            for obj in objects:
                json.dump(obj, f, ensure_ascii=False)
                f.write('\n')

        print(f"✓ Exported shader graph: {shader_path}")
        return shader_path

    def _extract_basecolor_value(self, unity_graph) -> dict:
        """Extract BaseColor value from converted nodes."""
        for node in unity_graph.nodes.values():
            bp = getattr(node, 'blender_props', {})
            # Look for Principled BSDF or color nodes
            if node.unity_name in ('Base Color', 'Principled BSDF') or bp.get('blender_type') == 'ShaderNodeBsdfPrincipled':
                # Try to get color from slots
                for slot in node.slots:
                    if slot.get('m_DisplayName') in ('Base Color', 'Color', 'BaseColor'):
                        val = slot.get('m_Value', {})
                        if isinstance(val, dict) and 'x' in val:
                            return val
            # Check for explicit color value
            color_val = bp.get('color')
            if color_val:
                return color_val
        # Default gray
        return {"x": 0.5, "y": 0.5, "z": 0.5}

    def _extract_metallic_value(self, unity_graph) -> float:
        """Extract Metallic value from converted nodes."""
        for node in unity_graph.nodes.values():
            bp = getattr(node, 'blender_props', {})
            if node.unity_name in ('Metallic', 'Principled BSDF') or bp.get('blender_type') == 'ShaderNodeBsdfPrincipled':
                for slot in node.slots:
                    if slot.get('m_DisplayName') in ('Metallic', 'MetallicScale'):
                        val = slot.get('m_Value')
                        if isinstance(val, (int, float)):
                            return float(val)
            metallic_val = bp.get('metallic')
            if metallic_val is not None:
                return float(metallic_val)
        return 0.0

    def _extract_smoothness_value(self, unity_graph) -> float:
        """Extract Smoothness value from converted nodes."""
        for node in unity_graph.nodes.values():
            bp = getattr(node, 'blender_props', {})
            if node.unity_name in ('Roughness', 'Principled BSDF') or bp.get('blender_type') == 'ShaderNodeBsdfPrincipled':
                for slot in node.slots:
                    if slot.get('m_DisplayName') in ('Roughness', 'Smoothness'):
                        val = slot.get('m_Value')
                        if isinstance(val, (int, float)):
                            return float(1.0 - val)  # Invert roughness to smoothness
            roughness_val = bp.get('roughness')
            if roughness_val is not None:
                return float(1.0 - roughness_val)
            smoothness_val = bp.get('smoothness')
            if smoothness_val is not None:
                return float(smoothness_val)
        return 0.5

    def _extract_emission_value(self, unity_graph) -> dict:
        """Extract Emission value from converted nodes."""
        for node in unity_graph.nodes.values():
            bp = getattr(node, 'blender_props', {})
            if node.unity_name in ('Emission', 'Principled BSDF') or bp.get('blender_type') == 'ShaderNodeBsdfPrincipled':
                for slot in node.slots:
                    if slot.get('m_DisplayName') == 'Emission':
                        val = slot.get('m_Value', {})
                        if isinstance(val, dict) and 'x' in val:
                            return val
            emission_val = bp.get('emission_strength')
            if emission_val:
                return {"x": emission_val, "y": emission_val, "z": emission_val}
        # Default black (no emission)
        return {"x": 0.0, "y": 0.0, "z": 0.0}

    # ── Material export ───────────────────────────────────────────────────────

    def export_material(self, shader_name: str, material_name: str, shader_guid: str = None, shader_type: str = 'UNIVERSAL'):
        """Export a Unity .mat file referencing the converted shader graph.
        
        Args:
            shader_name: Name of the shader graph (used for comment)
            material_name: Name of the material
            shader_guid: GUID of the exported shader graph file. If None, generates a new one.
            shader_type: One of 'UNIVERSAL', 'BUILTIN', or 'CUSTOM_RT'
        """
        safe_shader   = self._sanitize_name(shader_name)
        safe_material = self._sanitize_name(material_name)
        mat_path      = self.material_folder / f"{safe_material}.mat"
        
        # Use provided shader_guid or generate a new one
        if shader_guid is None:
            shader_guid = self._generate_guid()
        
        print(f"[DEBUG] Exporting material: {material_name} -> {mat_path}")

        # Determine shader reference based on shader_type
        if shader_type == 'UNIVERSAL':
            shader_file_id = -6465566751694194690  # URP Lit
        elif shader_type == 'BUILTIN':
            shader_file_id = -6465566751694194690  # Built-in Lit (same reference format)
        else:
            shader_file_id = -6465566751694194690  # Default to URP
        
        # Use the proper URP Shader Graph format with negative fileID
        content = (
            f"%YAML 1.1\n"
            f"%TAG !u! tag:unity3d.com,2011:\n"
            f"--- !u!21 &2100000\n"
            f"Material:\n"
            f"  serializedVersion: 8\n"
            f"  m_ObjectHideFlags: 0\n"
            f"  m_CorrespondingSourceObject: {{fileID: 0}}\n"
            f"  m_PrefabInstance: {{fileID: 0}}\n"
            f"  m_PrefabAsset: {{fileID: 0}}\n"
            f"  m_Name: {safe_material}\n"
            f"  m_Shader: {{fileID: {shader_file_id}, guid: {shader_guid}, type: 3}}\n"
            f"  m_Parent: {{fileID: 0}}\n"
            f"  m_ModifiedSerializedProperties: 0\n"
            f"  m_ValidKeywords: []\n"
            f"  m_InvalidKeywords: []\n"
            f"  m_LightmapFlags: 4\n"
            f"  m_EnableInstancingVariants: 0\n"
            f"  m_DoubleSidedGI: 0\n"
            f"  m_CustomRenderQueue: -1\n"
            f"  stringTagMap: {{}}\n"
            f"  disabledShaderPasses:\n"
            f"  - MOTIONVECTORS\n"
            f"  m_LockedProperties: \n"
            f"  m_SavedProperties:\n"
            f"    serializedVersion: 3\n"
            f"    m_TexEnvs:\n"
            f"    - _BaseMap:\n"
            f"        m_Texture: {{fileID: 0}}\n"
            f"        m_Scale: {{x: 1, y: 1}}\n"
            f"        m_Offset: {{x: 0, y: 0}}\n"
            f"    - _BumpMap:\n"
            f"        m_Texture: {{fileID: 0}}\n"
            f"        m_Scale: {{x: 1, y: 1}}\n"
            f"        m_Offset: {{x: 0, y: 0}}\n"
            f"    - _DetailAlbedoMap:\n"
            f"        m_Texture: {{fileID: 0}}\n"
            f"        m_Scale: {{x: 1, y: 1}}\n"
            f"        m_Offset: {{x: 0, y: 0}}\n"
            f"    - _DetailMask:\n"
            f"        m_Texture: {{fileID: 0}}\n"
            f"        m_Scale: {{x: 1, y: 1}}\n"
            f"        m_Offset: {{x: 0, y: 0}}\n"
            f"    - _DetailNormalMap:\n"
            f"        m_Texture: {{fileID: 0}}\n"
            f"        m_Scale: {{x: 1, y: 1}}\n"
            f"        m_Offset: {{x: 0, y: 0}}\n"
            f"    - _EmissionMap:\n"
            f"        m_Texture: {{fileID: 0}}\n"
            f"        m_Scale: {{x: 1, y: 1}}\n"
            f"        m_Offset: {{x: 0, y: 0}}\n"
            f"    - _MainTex:\n"
            f"        m_Texture: {{fileID: 0}}\n"
            f"        m_Scale: {{x: 1, y: 1}}\n"
            f"        m_Offset: {{x: 0, y: 0}}\n"
            f"    - _MetallicGlossMap:\n"
            f"        m_Texture: {{fileID: 0}}\n"
            f"        m_Scale: {{x: 1, y: 1}}\n"
            f"        m_Offset: {{x: 0, y: 0}}\n"
            f"    - _OcclusionMap:\n"
            f"        m_Texture: {{fileID: 0}}\n"
            f"        m_Scale: {{x: 1, y: 1}}\n"
            f"        m_Offset: {{x: 0, y: 0}}\n"
            f"    - _ParallaxMap:\n"
            f"        m_Texture: {{fileID: 0}}\n"
            f"        m_Scale: {{x: 1, y: 1}}\n"
            f"        m_Offset: {{x: 0, y: 0}}\n"
            f"    - _SpecGlossMap:\n"
            f"        m_Texture: {{fileID: 0}}\n"
            f"        m_Scale: {{x: 1, y: 1}}\n"
            f"        m_Offset: {{x: 0, y: 0}}\n"
            f"    - unity_Lightmaps:\n"
            f"        m_Texture: {{fileID: 0}}\n"
            f"        m_Scale: {{x: 1, y: 1}}\n"
            f"        m_Offset: {{x: 0, y: 0}}\n"
            f"    - unity_LightmapsInd:\n"
            f"        m_Texture: {{fileID: 0}}\n"
            f"        m_Scale: {{x: 1, y: 1}}\n"
            f"        m_Offset: {{x: 0, y: 0}}\n"
            f"    - unity_ShadowMasks:\n"
            f"        m_Texture: {{fileID: 0}}\n"
            f"        m_Scale: {{x: 1, y: 1}}\n"
            f"        m_Offset: {{x: 0, y: 0}}\n"
            f"    m_Ints: []\n"
            f"    m_Floats:\n"
            f"    - _AddPrecomputedVelocity: 0\n"
            f"    - _AlphaClip: 0\n"
            f"    - _AlphaToMask: 0\n"
            f"    - _Blend: 0\n"
            f"    - _BlendModePreserveSpecular: 1\n"
            f"    - _BumpScale: 1\n"
            f"    - _ClearCoatMask: 0\n"
            f"    - _ClearCoatSmoothness: 0\n"
            f"    - _Cull: 2\n"
            f"    - _Cutoff: 0.5\n"
            f"    - _DetailAlbedoMapScale: 1\n"
            f"    - _DetailNormalMapScale: 1\n"
            f"    - _DstBlend: 0\n"
            f"    - _DstBlendAlpha: 0\n"
            f"    - _EnvironmentReflections: 1\n"
            f"    - _GlossMapScale: 0\n"
            f"    - _Glossiness: 0\n"
            f"    - _GlossyReflections: 0\n"
            f"    - _Metallic: 0\n"
            f"    - _OcclusionStrength: 1\n"
            f"    - _Parallax: 0.005\n"
            f"    - _QueueControl: 0\n"
            f"    - _QueueOffset: 0\n"
            f"    - _ReceiveShadows: 1\n"
            f"    - _Smoothness: 0.5\n"
            f"    - _SmoothnessTextureChannel: 0\n"
            f"    - _SpecularHighlights: 1\n"
            f"    - _SrcBlend: 1\n"
            f"    - _SrcBlendAlpha: 1\n"
            f"    - _Surface: 0\n"
            f"    - _WorkflowMode: 1\n"
            f"    - _XRMotionVectorsPass: 1\n"
            f"    - _ZWrite: 1\n"
            f"    m_Colors:\n"
            f"    - _BaseColor: {{r: 1, g: 1, b: 1, a: 1}}\n"
            f"    - _Color: {{r: 1, g: 1, b: 1, a: 1}}\n"
            f"    - _EmissionColor: {{r: 0, g: 0, b: 0, a: 1}}\n"
            f"    - _SpecColor: {{r: 0.19999996, g: 0.19999996, b: 0.19999996, a: 1}}\n"
            f"  m_BuildTextureStacks: []\n"
            f"  m_AllowLocking: 1\n"
            f"--- !u!114 &1984901182601957524\n"
            f"MonoBehaviour:\n"
            f"  m_ObjectHideFlags: 11\n"
            f"  m_CorrespondingSourceObject: {{fileID: 0}}\n"
            f"  m_PrefabInstance: {{fileID: 0}}\n"
            f"  m_PrefabAsset: {{fileID: 0}}\n"
            f"  m_GameObject: {{fileID: 0}}\n"
            f"  m_Enabled: 1\n"
            f"  m_EditorHideFlags: 0\n"
            f"  m_Script: {{fileID: 11500000, guid: d0353a89b1f911e48b9e16bdc9f2e058, type: 3}}\n"
            f"  m_Name: \n"
            f"  m_EditorClassIdentifier: Unity.RenderPipelines.Universal.Editor::UnityEditor.Rendering.Universal.AssetVersion\n"
            f"  version: 10\n"
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

        fbx_helper.export_single_object_fbx(str(fbx_path))

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
            # Move to temp collection
            if obj.name in bpy.context.scene.collection.objects:
                bpy.context.scene.collection.objects.unlink(obj)
            temp_col.objects.link(obj)

        success = False
        try:
            bpy.ops.object.select_all(action='DESELECT')
            for obj in duplicated_objects:
                obj.select_set(True)
            bpy.context.view_layer.objects.active = duplicated_objects[0]

            fbx_helper.export_collection_fbx(str(fbx_path), duplicated_objects)
            success = True
        except Exception as e:
            print(f"Error exporting collection as FBX: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Deselect everything first
            bpy.ops.object.select_all(action='DESELECT')
            
            # Collect object names for safe iteration
            obj_names = [obj.name for obj in duplicated_objects]
            
            # Delete duplicated objects
            for obj_name in obj_names:
                if obj_name in bpy.data.objects:
                    try:
                        obj = bpy.data.objects[obj_name]
                        # Unlink from all collections
                        for col in obj.users_collection:
                            col.objects.unlink(obj)
                        # Delete the object
                        bpy.data.objects.remove(obj, do_unlink=True)
                    except Exception as cleanup_err:
                        print(f"Warning: Could not clean up object {obj_name}: {cleanup_err}")
            
            # Clean up temp collection
            if temp_col:
                try:
                    if temp_col.name in bpy.context.scene.collection.children:
                        bpy.context.scene.collection.children.unlink(temp_col)
                    if temp_col.name in bpy.data.collections:
                        bpy.data.collections.remove(temp_col)
                except Exception as cleanup_err:
                    print(f"Warning: Could not clean up temp collection: {cleanup_err}")

        if success:
            print(f"✓ Exported collection as FBX: {fbx_path}")
            return fbx_path
        return None

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
        """Sanitize a name for use as a file/asset name.
        
        Preserves Blender's .001, .002, etc. numbering to avoid name collisions.
        """
        name = str(name)
        # Only remove known file extensions, NOT Blender's .001, .002 numbering
        known_extensions = ('.blend', '.fbx', '.obj', '.png', '.jpg', '.jpeg', 
                           '.tga', '.exr', '.tif', '.tiff', '.svg', '.psd')
        
        # Check if name ends with Blender's numbering pattern like .001, .002
        has_blender_numbering = False
        if len(name) >= 4:
            import re
            if re.match(r'\.\d{3}$', name[-4:]):
                has_blender_numbering = True
        
        lower_name = name.lower()
        if not has_blender_numbering and any(lower_name.endswith(ext) for ext in known_extensions):
            # Remove the file extension
            name = os.path.splitext(name)[0]
        
        # Replace invalid characters, but keep dots if they are part of Blender numbering
        result = []
        for ch in name:
            if ch in r'\/:*?"<>| ':
                result.append('_')
            else:
                result.append(ch)
        name = ''.join(result)
        
        return name.strip('_') or "Exported"

    @staticmethod
    def _generate_guid() -> str:
        """Generate a 32-character hexadecimal GUID."""
        return uuid.uuid4().hex

    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp as ISO format string."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
