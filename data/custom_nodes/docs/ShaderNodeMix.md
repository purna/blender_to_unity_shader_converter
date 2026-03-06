# ShaderNodeMix

## Overview
- **Blender Node**: ShaderNodeMix
- **Category**: Utility
- **Compatibility**: 100%

## Conversion Process

### Step 1: Direct Port
- **Description**: Blends two values using Lerp (linear interpolation)
- **Blender Input**: A, B, Factor (0-1)
- **Unity Output**: Blended value

## Blender to Unity Mapping

| Blender Mode | Unity Implementation | Compatibility |
|--------------|---------------------|---------------|
| Mix (Lerp) | Lerp node | 100% |
| Add | Add | 100% |
| Subtract | Subtract | 100% |
| Multiply | Multiply | 100% |
| Screen | Screen blend | 100% |
| Overlay | Overlay blend | 100% |

## Build Instructions

1. Create Lerp node in Unity Shader Graph
2. Connect A and B inputs
3. Connect Factor (0-1) to T input
4. Connect output to destination

## Notes
- Direct 1:1 mapping to Unity Lerp
- Also supports Add, Subtract, Multiply blend modes
