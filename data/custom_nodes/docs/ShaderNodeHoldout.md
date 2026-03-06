# ShaderNodeHoldout

## Overview
- **Blender Node**: ShaderNodeHoldout
- **Category**: Shader
- **Compatibility**: 5%

## Conversion Process

### Step 1: Identify Holdout Usage
- **Description**: Determine how holdout is used in the Blender shader (compositing or surface)
- **Blender Input**: Holdout shader
- **Unity Output**: Determine appropriate replacement

### Step 2: Replace with Alpha Cutout
- **Description**: Use Alpha Clip threshold to create holdout effect
- **Blender Input**: Holdout surface
- **Unity Output**: Alpha = 0, Alpha Clip Threshold

### Step 3: Manual Adjustments
- **Description**: Fine-tune the cutout edge
- **Blender Input**: Holdout mask
- **Unity Output**: Adjust Alpha Clip Threshold as needed

## Blender to Unity Mapping

| Blender Parameter | Unity Implementation | Compatibility |
|-------------------|---------------------|---------------|
| Color | Alpha = 0, Alpha Clip Threshold | 5% |

## Build Instructions

1. Create Alpha Clip Threshold in Shader Graph
2. Set Alpha to 0 for held-out areas
3. Connect mask to Alpha Clip Threshold
4. Enable Alpha Clipping in Graph Settings
5. Adjust threshold for desired edge quality

## Notes
- Holdout is a compositing node in Blender with no real-time equivalent
- Can be approximated using Alpha Clipping
- This is fundamentally a compositing operation, not a surface shading one
