# ShaderNodeBsdfSheen - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Shader
- **Compatibility**: 30%

## Blender Node Description
Fabric sheen shader - complex BSDF model with limited Unity support. Sheen creates a soft edge glow characteristic of fabrics like velvet or satin.

## Unity Equivalent
- **Primary**: PBR Master Sheen (URP/HDRP only)
- **Fallback**: Fresnel approximation

## Conversion Process

### Step 1: Check Unity Version
- URP/HDRP has built-in Sheen support in PBR Master
- Built-in/Standard pipeline requires custom approximation

### Step 2: URP/HDRP Path
- Enable Sheen in PBR Master node
- Connect Color to Sheen Tint
- Connect Roughness to Sheen Smoothness (inverted)

### Step 3: Standard/Built-in Path
- Use Fresnel node for edge glow approximation
- Multiply Fresnel output by sheen color
- Connect to Emission or Base Color

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Color | Color | Sheen Color | URP/HDRP only |
| Roughness | Float | Sheen Smoothness | Inverted (1-Roughness) |

## Compatibility Notes
- Fundamentally different rendering model
- URP/HDRP provides native Sheen support
- Built-in pipeline requires custom shader code

## Limitations
- No native Sheen BSDF in standard Unity
- Approximations are imperfect
- Visual result may differ from Blender
