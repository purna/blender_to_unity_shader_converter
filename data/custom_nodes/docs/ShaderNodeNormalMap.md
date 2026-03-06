# ShaderNodeNormalMap

## Overview
- **Blender Node**: ShaderNodeNormalMap
- **Category**: Vector
- **Compatibility**: 90%

## Conversion Process

### Step 1: Sample Normal Map
- **Description**: Sample the normal map texture with Type=Normal
- **Blender Input**: Normal map texture (RGB)
- **Unity Output**: RGB color from texture

### Step 2: Connect to Normal Map Node
- **Description**: Connect texture to Normal From Texture node
- **Blender Input**: RGB texture output
- **Unity Output**: Normal vector

### Step 3: Apply Strength
- **Description**: Adjust normal strength if needed
- **Blender Input**: Strength parameter
- **Unity Output**: Adjusted normal

## Blender to Unity Mapping

| Blender Parameter | Unity Implementation | Compatibility |
|-------------------|---------------------|---------------|
| Color | Sample Texture 2D (Type: Normal) | 100% |
| Strength | Multiply normal effect | 90% |
| Space | Space selection | 90% |

## Build Instructions

1. Create Sample Texture 2D node
2. Set Type to "Normal"
3. Connect to Normal From Texture node (or use inline)
4. Connect output to PBR Normal input

## Notes
- Direct mapping to Unity normal map workflow
- 10% loss due to minor encoding differences
- Supports Tangent, Object, World spaces
