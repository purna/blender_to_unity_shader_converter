# ShaderNodeBsdfPrincipled

## Overview
Blender's universal physically-based shader that covers most material types. This is the most complex conversion as it has many parameters.

## Unity Equivalent
- **Primary**: PBR Master (Lit) - covers 90% of use cases
- **Advanced**: Custom shader for subsurface, clearcoat, sheen

## Conversion Process

### Step 1: Basic PBR Mapping (90%)
| Blender Parameter | Unity Input | Notes |
|-----------------|-------------|-------|
| Base Color | Base Color | Direct mapping |
| Metallic | Metallic | 0-1 float |
| Roughness | Smoothness | Invert: 1-Roughness |
| Normal | Normal | Connect normal map |
| Emission | Emission | Color × Strength |

### Step 2: Unsupported Features (10%)
- **Subsurface Scattering**: Approximate with translucent or custom SSS shader
- **Clearcoat**: Add second specular layer if needed
- **Sheen**: Use Sheen in PBR Master (URP/HDRP)
- **Transmission**: Use Transparent surface type

## Compatibility: 50% (due to advanced features)

## Limitations
- SSS requires custom implementation
- Clearcoat/Coat not directly supported
- Advanced transmission needs custom shader
- IOR calculations differ
