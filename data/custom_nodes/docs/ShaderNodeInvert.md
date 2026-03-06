# ShaderNodeInvert

## Overview
- **Blender Node**: ShaderNodeInvert
- **Category**: Utility
- **Compatibility**: 100%

## Conversion Process

### Step 1: Direct Port
- **Description**: Invert color or value using simple subtraction (1 - value)
- **Blender Input**: Color or Factor
- **Unity Output**: Inverted color/value

## Blender to Unity Mapping

| Blender Parameter | Unity Implementation | Compatibility |
|-------------------|---------------------|---------------|
| Color | Input to One Minus | 100% |
| Factor | Blend with inverted value | 100% |

## Build Instructions

1. Create One Minus node in Unity Shader Graph
2. Connect color or value to One Minus input
3. For Factor blending: Use Lerp between original and inverted
4. Connect output to destination

## Notes
- Fully compatible - direct 1:1 mapping
- Unity's One Minus node performs exactly the same operation
- For factor-based inversion: Lerp(Color, 1-Color, Factor)
