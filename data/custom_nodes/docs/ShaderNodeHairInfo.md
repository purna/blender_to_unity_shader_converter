# ShaderNodeHairInfo

## Overview
- **Blender Node**: ShaderNodeHairInfo
- **Category**: Input
- **Compatibility**: 20%

## Conversion Process

### Step 1: Identify Hair Information Needs
- **Description**: Analyze what hair strand information is used in the Blender shader
- **Blender Input**: Hair strand data (position, tangent, length, etc.)
- **Unity Output**: Determine which outputs are needed

### Step 2: Create Approximation Nodes
- **Description**: Approximate hair information using available Unity nodes
- **Blender Input**: Hair Info outputs (Strand Tangent, Intercept, etc.)
- **Unity Output**: Vertex Color, UV coordinates, or custom attributes

### Step 3: Custom Shader Implementation (If Needed)
- **Description**: For advanced hair rendering, create custom HLSL
- **Blender Input**: Full hair strand data
- **Unity Output**: Custom hair shader with vertex attributes

## Blender to Unity Mapping

| Blender Parameter | Unity Implementation | Compatibility |
|-------------------|---------------------|---------------|
| Strand Tangent | Normal Vector or Tangent | 30% |
| Intercept | UV or custom attribute | 20% |
| Length | Approximate via scaling | 10% |
| Random | Vertex Color (randomized) | 20% |

## Build Instructions

1. Analyze hair shader requirements in Blender
2. Export hair geometry with appropriate vertex colors or UVs
3. In Unity Shader Graph, use Vertex Color node for randomization
4. For strand-based effects, use custom HLSL code
5. Consider using Unity's Hair Render Pipeline or VF graph for complex hair

## Notes
- Limited compatibility - hair strand information is specific to Blender's hair system
- Unity does not have a direct Hair Info node
- Use vertex colors or custom attributes to approximate
- Consider using Unity's dedicated hair solutions for production
