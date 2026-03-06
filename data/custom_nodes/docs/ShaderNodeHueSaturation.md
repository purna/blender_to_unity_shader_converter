# ShaderNodeHueSaturation

## Overview
- **Blender Node**: ShaderNodeHueSaturation
- **Category**: Color
- **Compatibility**: 70%

## Conversion Process

### Step 1: Convert RGB to HSV
- **Description**: Convert input color from RGB to HSV color space
- **Blender Input**: RGB Color
- **Unity Output**: HSV values (Hue, Saturation, Value)

### Step 2: Apply Adjustments
- **Description**: Apply Hue, Saturation, and Value modifications
- **Blender Input**: Hue (0-360°), Saturation (0-2), Value (0-1)
- **Unity Output**: Adjusted HSV

### Step 3: Convert Back to RGB
- **Description**: Convert modified HSV back to RGB color space
- **Blender Input**: Adjusted HSV
- **Unity Output**: RGB Color

## Blender to Unity Mapping

| Blender Parameter | Unity Implementation | Compatibility |
|-------------------|---------------------|---------------|
| Color | Input Color | 100% |
| Hue | HSV Node Hue (0-1) | 80% |
| Saturation | HSV Node Saturation | 70% |
| Value | HSV Node Value | 70% |

## Build Instructions

1. Create HSV node in Unity Shader Graph
2. Connect color to HSV node input
3. Adjust Hue, Saturation, and Value inputs
4. Connect output to desired destination

## Notes
- Unity has a built-in HSV node that handles RGB-HSV conversion internally
- Blender Hue range is 0-360°, Unity is 0-1 (need to divide by 360)
- Blender Saturation default is 1, can go from 0-2; Unity handles similarly
- For exact matches, create custom function nodes
