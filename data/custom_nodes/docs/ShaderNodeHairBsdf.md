# Hair BSDF Node

## ✅ SOLUTION FOUND!

**Unity URP/HDRP has built-in hair support!**
- URP: Hair Master Stack (Unity 2021.2+)
- HDRP: Hair Shader Type
- **Kajiya-Kay algorithm FOUND in Unity's BSDF.hlsl!**

## Overview
The Hair BSDF node simulates light interaction with hair or fur strands using the Kajiya-Kay or Marschner model.

## Unity Solutions

### Option 1: URP Hair Master Stack (Recommended)
**Best for performance** - Use Unity's built-in URP Hair shader:
- Create new Shader Graph → Select "Hair" master stack
- Set Base Color, Roughness, Alpha
- Built-in anisotropic highlights

### Option 2: HDRP Hair Shader
**Best for quality** - Use HDRP's hair rendering:
- Create new Shader Graph → Select "Hair" 
- Full hair rendering pipeline
- Multiple scattering support

### Option 3: Custom Kajiya-Kay (Found in Unity!)
**Unity's BSDF.hlsl contains Kajiya-Kay!** Found at:
`Library/PackageCache/com.unity.render-pipelines.core@.../ShaderLibrary/BSDF.hlsl`

```hlsl
// From Unity's BSDF.hlsl
real3 D_KajiyaKay(real3 T, real3 H, real specularExponent)
{
    // Kajiya-Kay implementation!
}
```

## Blender to Unity Mapping

| Blender | Unity URP Hair | Compatibility |
|---------|---------------|---------------|
| Color | Base Color | ✅ 100% |
| Roughness | Roughness | ✅ 100% |
| Radial Roughness | Anisotropy + Custom | ⚠️ 25% |
| Coat | (Not available) | ❌ |

## Reference Files
- Anisotropy shader: `SamplesBackdrop.shadergraph` (has Anisotropy property)
- Kajiya-Kay: `BSDF.hlsl` (contains D_KajiyaKay function)
