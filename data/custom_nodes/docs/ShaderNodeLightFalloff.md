# ShaderNodeLightFalloff

## Overview
- **Blender Node**: ShaderNodeLightFalloff
- **Category**: Shader
- **Compatibility**: 0%

## Conversion Process

### Step 1: Identify Light Falloff Requirements
- **Description**: This node controls light attenuation curves - not supported in real-time
- **Blender Input**: Light falloff parameters
- **Unity Output**: N/A - cannot be directly converted

### Step 2: Use Constant Values
- **Description**: Replace with constant values or material properties
- **Blender Input**: Quadratic/Linear/Constant falloff
- **Unity Output**: Fixed values or custom shader code

### Step 3: Custom Shader (Advanced)
- **Description**: For complex falloff, write custom HLSL
- **Blender Input**: Custom falloff curve
- **Unity Output**: Custom attenuation shader

## Blender to Unity Mapping

| Blender Parameter | Unity Implementation | Compatibility |
|-------------------|---------------------|---------------|
| Quadratic | Custom HLSL only | 0% |
| Linear | Custom HLSL only | 0% |
| Constant | Constant value | 0% |

## Build Instructions

1. This node has no direct Unity equivalent
2. Replace with constant values based on desired falloff
3. For advanced lighting, use custom HLSL in a Custom Function node
4. Consider using Unity's lighting system for distance-based attenuation

## Notes
- Light falloff is a Cycles-specific feature unavailable in real-time rendering
- Unity's real-time rendering handles light attenuation automatically
- This node is fundamentally incompatible with real-time rendering pipelines
