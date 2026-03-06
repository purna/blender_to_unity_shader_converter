# ShaderNodeBsdfVelvet - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Shader
- **Compatibility**: 50%

## Blender Node Description
Velvet shader with edge sheen. Creates characteristic soft edge glow of velvet fabrics.

## Unity Equivalent
- **Primary**: Fresnel approximation
- **Implementation**: Fresnel × Color

## Conversion Process

### Step 1: Create Fresnel Node
- Add Fresnel node
- Set Power/Intensity to control edge glow

### Step 2: Multiply with Color
- Create Multiply node
- Connect Fresnel output × Velvet Color

### Step 3: Connect to Output
- Connect result to Emission or Base Color

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Color | Color | Multiply with Fresnel | Approximation |

## Compatibility Notes
- Fresnel approximation provides similar edge effect
- 50% compatible - imperfect match

## Limitations
- No native Velvet BSDF
- Imperfect approximation
- Different falloff curve
