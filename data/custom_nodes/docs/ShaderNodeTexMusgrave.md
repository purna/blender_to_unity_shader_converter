# ShaderNodeTexMusgrave - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Texture
- **Compatibility**: 40%

## Blender Node Description
Musgrave Texture - procedural fractal noise with various fractal types (Multifractal, Ridged, Hybrid, Domain Warped, FBM).

## Unity Equivalent
- **Primary**: Custom Function
- **Implementation**: Requires custom HLSL or noise approximation

## Conversion Process

### Step 1: Create Noise Base
- Use Unity's Simple Noise node
- Set appropriate scale

### Step 2: Add Fractal
- Add multiple noise octaves
- Use Add node to combine

### Step 3: Configure Type
- Use different combinations per type
- Domain Warping requires complex setup

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Vector | Vector | UV | Direct |
| Scale | Float | Scale | Direct |
| Detail | Float | Octaves | Partial |
| Dimension | Float | Lacunarity | Partial |
| Offset | Float | Offset | Partial |
| Gain | Float | Gain | Partial |

## Compatibility Notes
- 40% compatible - requires approximation
- Complex fractal types need custom code

## Limitations
- Domain Warping not available
- Different noise algorithms
