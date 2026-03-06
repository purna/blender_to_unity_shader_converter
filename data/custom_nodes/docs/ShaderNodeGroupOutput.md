# ShaderNodeGroupOutput

## Overview
- **Blender Node**: ShaderNodeGroupOutput
- **Category**: Output
- **Compatibility**: 100%

## Conversion Process

### Step 1: Direct Port
- **Description**: Group output node is a structural node that simply exposes outputs from a node group
- **Blender Input**: N/A (structural node)
- **Unity Output**: Group Output node in Shader Graph

## Blender to Unity Mapping

| Blender Parameter | Unity Implementation | Compatibility |
|-------------------|---------------------|---------------|
| Surface | Fragment Output (Base Color, Alpha) | 100% |
| Displacement | Disconnect or use Master Position | 100% |
| Emission | Emission | 100% |

## Build Instructions

1. Create Group Output node in Shader Graph
2. Connect shader outputs to the appropriate input slots
3. For Surface: Connect to Base Color, Normal, Metallic, Smoothness, etc.
4. For Emission: Connect to Emission input

## Notes
- Fully compatible - direct 1:1 mapping
- Used to expose outputs from node groups in both Blender and Unity
