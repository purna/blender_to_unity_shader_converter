# ShaderNodeMapRange

## Overview
- **Blender Node**: ShaderNodeMapRange
- **Category**: Utility
- **Compatibility**: 90%

## Conversion Process

### Step 1: Direct Mapping
- **Description**: Map input value from source range to target range
- **Blender Input**: Value, FromMin, FromMax, ToMin, ToMax
- **Unity Output**: Remapped value

### Step 2: Apply Clamp (Optional)
- **Description**: Optionally clamp output to target range
- **Blender Input**: Clamp mode setting
- **Unity Output**: Clamped or unclamped output

## Blender to Unity Mapping

| Blender Parameter | Unity Implementation | Compatibility |
|-------------------|---------------------|---------------|
| Value | Input Value | 100% |
| From Min | Remap From Min | 100% |
| From Max | Remap From Max | 100% |
| To Min | Remap To Min | 100% |
| To Max | Remap To Max | 100% |
| Clamp | Built-in clamp option | 90% |

## Build Instructions

1. Create Remap node in Unity Shader Graph
2. Connect input value to Remap node
3. Set From Min/Max to match Blender
4. Set To Min/Max to match Blender
5. Enable Clamp if needed in Remap settings

## Formula
```
output = (input - fromMin) / (fromMax - fromMin) * (toMax - toMin) + toMin
```

## Notes
- Direct 1:1 mapping to Unity Remap node
- Unity's Remap node handles the formula internally
- Blender has interpolation curve option; standard Remap is linear only
- 10% loss due to lack of non-linear interpolation curves
