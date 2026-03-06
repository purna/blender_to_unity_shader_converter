# ShaderNodeBsdfToon - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Shader
- **Compatibility**: 40%

## Blender Node Description
Toon/cel-shaded shader - stylized rendering with stepped lighting. Creates discrete light bands for cartoon-like appearance.

## Unity Equivalent
- **Primary**: Custom Unlit with Sample Gradient
- **Implementation**: Dot Product + Sample Gradient for stepped effect

## Conversion Process

### Step 1: Calculate Lighting
- Create Dot Product node (Normal × Light Direction)
- Get Light Direction from Main Light node or use default vector

### Step 2: Apply Gradient Ramp
- Connect Dot Product result to Sample Gradient input
- Create gradient with hard stops for toon effect
- Adjust gradient positions to control band size

### Step 3: Apply Color
- Multiply gradient result by base color
- Connect to emission or base color output

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Color | Color | Base Color | Multiply with gradient |
| Size | Float | Gradient Stops | Adjust gradient positions |

## Compatibility Notes
- No native toon shader in ShaderGraph
- Requires custom gradient setup
- Single light only in simple implementations

## Limitations
- Requires custom gradient setup
- Light direction must be calculated
- May need custom shader for multiple lights
