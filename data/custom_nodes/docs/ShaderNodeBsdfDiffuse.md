# ShaderNodeBsdfDiffuse

## Overview
| Property | Value |
|----------|-------|
| **Source** | Blender Cycles/Eevee |
| **Target** | Unity URP/HDRP |
| **Compatibility** | 85% |
| **Category** | Shader |
| **Complexity** | Medium |

## Summary
Lambertian diffuse shader. Blender uses BSDF model; Unity Lit shader achieves same result by setting Smoothness=0 and Metallic=0.

## Unity Equivalent
**Standard Diffuse** - PBR Master with specific settings

## Conversion Process

### Step 1: Set Base Color
- **Blender Input**: Color
- **Unity Output**: Base Color on PBR Master
- **Description**: Connect diffuse color to Base Color input

### Step 2: Handle Normal
- **Blender Input**: Normal
- **Unity Output**: Normal input on PBR Master
- **Description**: Connect normal map if present

### Step 3: Configure PBR
- **Blender Input**: Roughness
- **Unity Output**: Smoothness (inverted)
- **Description**: Unity_Smoothness = 1.0 - Blender_Roughness
- **Note**: Set Metallic = 0.0 for pure diffuse

## Parameters
| Blender | Description | Unity Mapping |
|---------|-------------|--------------|
| Color | Diffuse surface color | → Base Color |
| Normal | Surface normal | → Normal input |
| Roughness | Surface roughness | → Smoothness = 1-Roughness |

## Roughness Conversion
| Blender Roughness | Unity Smoothness |
|-------------------|------------------|
| 0.0 | 1.0 (mirror) |
| 0.5 | 0.5 (default) |
| 1.0 | 0.0 (matte) |

## Compatibility
- **Fully Compatible**: Basic diffuse lighting
- **Partially Compatible**: Advanced BSDF features
- **Incompatible**: Blender BSDF fresnel behavior at extreme angles

## Limitations
- Blender BSDF fresnel behavior differs slightly from Lambertian at extreme angles
- 15% compatibility loss due to fresnel differences
