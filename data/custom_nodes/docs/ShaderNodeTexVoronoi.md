# ShaderNodeTexVoronoi - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Texture
- **Compatibility**: 60%

## Blender Node Description
Voronoi Texture - procedural cellular/crystal pattern with distance metrics and feature weights.

## Unity Equivalent
- **Primary**: Voronoi Node
- **Implementation**: Partial support with Unity's Voronoi

## Conversion Process

### Step 1: Create Voronoi
- Add Voronoi node in Unity ShaderGraph

### Step 2: Configure Parameters
- Set scale for cell size
- Connect UV input

### Step 3: Adjust Output
- Use Distance output for cell edges
- Use Color output for cell colors

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Vector | Vector | UV | Direct |
| Scale | Float | Scale | Direct |
| Randomness | Float | Jitter | Partial |

## Compatibility Notes
- 60% compatible - basic Voronoi works
- Distance metrics differ

## Limitations
- Different distance metrics
- Less randomness control
