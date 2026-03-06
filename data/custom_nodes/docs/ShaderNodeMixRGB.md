# ShaderNodeMixRGB

## Overview
- **Blender Node**: ShaderNodeMixRGB
- **Category**: Color
- **Compatibility**: 90%

## Conversion Process

### Step 1: Select Blend Mode
- **Description**: Choose the appropriate blend operation
- **Blender Input**: Color1, Color2, Factor, Mode
- **Unity Output**: Blended color

### Step 2: Apply Blend
- **Description**: Use appropriate Unity node for the blend mode
- **Blender Input**: Blend mode selection
- **Unity Output**: Blended result

## Blender to Unity Mapping

| Blender Mode | Unity Implementation | Compatibility |
|--------------|---------------------|---------------|
| Mix | Lerp | 100% |
| Darken | Min | 100% |
| Multiply | Multiply | 100% |
| Lighten | Max | 100% |
| Screen | Screen formula | 100% |
| Add | Add | 100% |
| Overlay | Custom function | 80% |
| Soft Light | Custom function | 80% |

## Build Instructions

1. Identify blend mode in Blender
2. Create appropriate Unity node (Lerp, Add, Multiply, etc.)
3. Connect colors and factor
4. For Overlay/Soft Light, use Custom Function node

## Notes
- Most blend modes map directly
- Overlay and Soft Light require custom functions for exact match
- 10% loss due to complex blend mode differences
