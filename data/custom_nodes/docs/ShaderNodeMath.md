# ShaderNodeMath

## Overview
- **Blender Node**: ShaderNodeMath
- **Category**: Utility
- **Compatibility**: 100%

## Conversion Process

### Step 1: Direct Operation Mapping
- **Description**: All math operations map directly to Unity Math node
- **Blender Input**: Math operation (Add, Multiply, Divide, etc.)
- **Unity Output**: Same operation in Unity

## Blender to Unity Mapping

| Blender Operation | Unity Operation | Compatibility |
|------------------|-----------------|---------------|
| ADD | Add | 100% |
| SUBTRACT | Subtract | 100% |
| MULTIPLY | Multiply | 100% |
| DIVIDE | Divide | 100% |
| POWER | Power | 100% |
| LOGARITHM | Log | 100% |
| SQRT | Sqrt | 100% |
| ABSOLUTE | Abs | 100% |
| MINIMUM | Min | 100% |
| MAXIMUM | Max | 100% |
| MODULO | Fmod | 100% |
| FLOOR | Floor | 100% |
| CEIL | Ceil | 100% |
| FRACTION | Frac | 100% |

## Build Instructions

1. Create Math node in Unity Shader Graph
2. Set Operation property to match Blender
3. Connect Value1 and Value2 inputs
4. Connect output to destination

## Notes
- Perfect 1:1 mapping for all operations
- Direct port to Unity Math node
- Use Clamp option if needed
