# ShaderNodeBsdfGlossy

## Overview
Blender's glossy/reflective BSDF shader node for creating shiny surfaces like plastic, metal, or polished materials.

## Unity Equivalent
- **Primary**: PBR Master (Lit) with high smoothness
- **Alternative**: Custom shader with GGX distribution

## Conversion Process

### Step 1: Basic Material Setup
1. Create a new PBR Master (Lit) node in Unity ShaderGraph
2. Set Surface Type to Opaque

### Step 2: Map Parameters
| Blender Input | Unity Input | Notes |
|--------------|-------------|-------|
| Color | Base Color | Specular color (often white for dielectric) |
| Roughness | Smoothness | Invert: Smoothness = 1 - Roughness |

### Step 3: Distribution Handling
- Blender's GGX distribution maps directly to Unity's default PBR
- Beckmann/Ashikhmin approximations use GGX (visually similar)

## Compatibility: 70%

## Limitations
- Different BRDF models between engines
- Extreme angles may show slight differences
- Distribution selection not available in standard ShaderGraph
