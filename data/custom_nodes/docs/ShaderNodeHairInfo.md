# ShaderNodeHairInfo

## Overview
- **Blender Node**: ShaderNodeHairInfo
- **Category**: Input
- **Compatibility**: 30%

## ✅ EXAMPLES FOUND!

Unity ShaderGraph has hair shader examples:

| Example | Path |
|---------|------|
| **NormalBlend** | [`NormalBlend.shadergraph`](../../examples/ShaderNodeHairInfo/NormalBlend.shadergraph) |

## Unity Hair Strand Direction

Unity ShaderGraph supports **Hair Strand Direction** in the Vertex Stage:

```
Vertex Stage > Hair Strand Direction
```

This provides access to hair strand tangent information for strand-based rendering.

## Blender to Unity Mapping

| Blender Output | Unity Implementation | Compatibility |
|---------------|---------------------|---------------|
| Strand Tangent | Hair Strand Direction | ✅ 30% |
| Intercept | Custom UV or Attribute | 20% |
| Length | Vertex scaling | 10% |
| Random | Vertex Color | 20% |

## Conversion Process

### Unity Hair Shader Approach

1. **Use Vertex Stage** - Access Hair Strand Direction property
2. **Connect to Normal** - Use for strand-based lighting
3. **Custom Attributes** - Set up custom vertex data for complex hair

## Notes
- Unity has built-in Hair Strand Direction in Vertex Stage
- Cannot access Blender's live hair simulation
- Use Vertex Color for randomization
- Consider Unity's Hair Render Pipeline for production
