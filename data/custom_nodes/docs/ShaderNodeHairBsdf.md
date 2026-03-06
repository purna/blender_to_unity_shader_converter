# Hair BSDF Node

## Overview
The Hair BSDF node simulates light interaction with hair or fur strands. It models the reflection and transmission of light through hair fibers using physically-based shading.

## Blender Node Inputs
- **Color**: Hair color (RGB)
- **Roughness**: Surface roughness (0-1)
- **Radial Roughness**: Radial roughness for anisotropic highlights (0-1)
- **Coat**: Additional layer intensity
- **Offset**: Hair strand offset angle
- **Direct**: Direct lighting strength
- **Indirect**: Indirect/ambient lighting strength

## Blender Node Outputs
- **BSDF**: Shader output (connecting to Mix Shader or Output)

## Unity Equivalent

### The Challenge
Unity's built-in render pipeline doesn't have a native hair shader. Options include:

### Option 1: Unity Hair Strand Shader (URP/HDRP)
**URP**: Use the "Hair" master stack (Unity 2021.2+)
- Built-in hair rendering
- Anisotropic highlights
- Alpha transparency for strands

**HDRP**: Use "Hair" shader type
- Full hair rendering pipeline
- Multiple scattering
- Instance-based rendering

### Option 2: Custom Hair Shader
Create custom shader with Kajiya-Kay or Marschner model:

```hlsl
// Simplified Kajiya-Kay Hair Shader
float3 HairShading(float3 N, float3 V, float3 L, float3 hairDir, float3 hairColor, float roughness)
{
    float3 T = normalize(hairDir);  // Tangent along hair
    
    // Kajiya-Kay diffuse
    float TdotL = dot(T, L);
    float TdotV = dot(T, V);
    float diffuse = sqrt(max(0, 1 - TdotL * TdotL));
    
    // Specular (anisotropic highlight)
    float spec = pow(max(0, sin(TdotL) * cos(TdotV) - TdotL * TdotV * 0.5), 1 / roughness);
    
    return hairColor * diffuse + spec * 0.5;
}
```

### Option 3: Approximation with Standard Shader
For simple hair rendering:
1. Use Standard Shader with Anisotropic
2. Set "Anisotropic" mode in material
3. Use UVs aligned to hair direction
4. Adjust "Shift" for highlight control

## Conversion Strategy

### High-Quality Approach (URP/HDRP)
1. Use Unity's built-in Hair shader
2. Convert hair curves to mesh/strands
3. Assign material with hair properties
4. Adjust parameters to match Blender

### Approximation Approach (Built-in/URP)
1. Create geometry (thin strips or planes)
2. Use Standard shader with:
   - Anisotropic enabled
   - Low smoothness
   - Alpha clipping for strand effect
3. Add alpha texture for strand pattern

### Vertex Animation Approach
```hlsl
// Simple hair strand movement
float3 OffsetHair(float3 position, float time)
{
    float offset = sin(time * 2 + position.y * 10) * 0.1;
    return position + float3(offset, 0, 0);
}
```

## Parameter Mapping

| Blender | Unity URP Hair | Approximation |
|---------|----------------|----------------|
| Color | Base Color | Albedo |
| Roughness | Roughness | Smoothness (inverted) |
| Radial Roughness | Radial Roughness | Anisotropic (manual) |
| Coat | Coat | Custom |
| Offset | Shift | Rotation |

## Compatibility
- **Compatibility**: 10%
- **Notes**: Complex to replicate. Requires Unity's hair pipeline or custom shader development. Direct geometry export recommended.

## Workflow Recommendations

### Best Practice: Use Unity's Hair System
1. Model hair as curves in Blender
2. Convert curves to mesh in Unity (using packages)
3. Apply Unity Hair material
4. Fine-tune parameters

### Export Approach
1. Export hair as geometry (strips/planes)
2. Bake hair data to texture (color, length)
3. Import to Unity
4. Apply custom or built-in hair shader

### For Real-time Applications
- Use alpha clipping for strand effect
- Use vertex animation for movement
- Pre-bake ambient occlusion

## Additional Resources
- [Unity URP Hair Shader Documentation](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest/index.html?subfolder=/manual/Hair-Master-Stack.html)
- [Marschner Hair Model](https://www.graphics.stanford.edu/papers/hair/)
- [Kajiya-Kay Hair Shading](https://developer.nvidia.com/hair-and-fur-rendering-and-simulation)
- [Blender Hair BSDF Node](https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/hair.html)
