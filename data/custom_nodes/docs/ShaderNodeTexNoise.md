# ShaderNodeTexNoise - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Texture
- **Compatibility**: 80%

## Blender Node Description
Noise Texture - procedural Perlin or Voronoi noise with adjustable scale, detail, and roughness.

## Unity Equivalent
- **Primary**: Simple Noise Node
- **Implementation**: Direct mapping for basic noise

## Conversion Process

### Step 1: Create Simple Noise
- Add Simple Noise node in Unity
- Connect UV

### Step 2: Configure Scale
- Set Scale for noise frequency

### Step 3: Add Detail
- Add multiple octaves using fractal
- Use for more detail

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Vector | Vector | UV | Direct |
| Scale | Float | Scale | Direct |
| Detail | Float | Octaves | Partial |
| Roughness | Float | Lacunarity | Partial |

## Compatibility Notes
- 80% compatible - basic noise works
- Different noise algorithm

## Limitations
- Different noise implementation
- Less control than Blender
