# ShaderNodeBsdfAnisotropic

## Overview
| Property | Value |
|----------|-------|
| **Source** | Blender Cycles/Eevee |
| **Target** | Unity URP/HDRP |
| **Compatibility** | 30% |
| **Category** | Shader |

## Summary
Anisotropic specular highlights - directional roughness for materials like brushed metal.

## Unity Equivalent
**Anisotropy** in PBR Master (URP/HDRP) or Custom shader

## Conversion Process

### Step 1: Set Base Color
- **Blender Input**: Color
- **Unity Output**: Base Color on PBR Master
- **Description**: Connect color to material base color

### Step 2: Configure Roughness
- **Blender Input**: Roughness X/Y
- **Unity Output**: Anisotropy on PBR Master
- **Description**: Use anisotropic roughness with different X/Y values

### Step 3: Set Rotation
- **Blender Input**: Rotation
- **Unity Output**: Tangent output
- **Description**: Configure tangent direction for anisotropy direction

### Step 4: Connect to Master
- **Blender Input**: BSDF output
- **Unity Output**: PBR Master
- **Description**: Connect to Lit shader

## Parameters
| Blender | Description |
|---------|-------------|
| Color | Surface color |
| Roughness X | Roughness in U direction |
| Roughness V | Roughness in V direction |
| Rotation | Anisotropy rotation angle |

## Unity Implementation
- Use PBR Master (URP/HDRP)
- Enable Anisotropy property
- Set Tangent direction

## Compatibility
- **Fully Compatible**: None (limited support)
- **Partially Compatible**: Basic anisotropic highlights
- **Incompatible**: Complex anisotropic workflows

## Limitations
- Very limited support in Unity
- Requires custom shader for full functionality
- May need manual setup in shader code
