# ShaderNodeOutputMaterial

## Overview
- **Blender Node**: ShaderNodeOutputMaterial
- **Category**: Output
- **Compatibility**: 100%

## Conversion Process

### Step 1: Direct Port
- **Description**: Material output node - maps to Master Stack in Unity
- **Blender Input**: BSDF/Shader, Displacement, Normal
- **Unity Output**: Fragment output

## Blender to Unity Mapping

| Blender Parameter | Unity Implementation | Compatibility |
|-------------------|---------------------|---------------|
| Surface | Fragment Output (Base Color, etc.) | 100% |
| Displacement | Master Position | 100% |
| Normal | Normal input | 100% |

## Build Instructions

1. Create Master Stack / Fragment output in Unity
2. Connect Base Color, Metallic, Smoothness, etc.
3. Connect Normal to Normal input
4. Connect displacement to Position if supported

## Notes
- Fully compatible - direct 1:1 mapping
- Terminal node in both Blender and Unity
- All material properties map to PBR Master
