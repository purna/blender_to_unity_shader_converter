# ShaderNodeBsdfRefraction

## Overview
Blender's refraction BSDF for transparent materials like glass and water that bend light.

## Unity Equivalent
- **Primary**: Transparent PBR with IOR
- **Approximation**: Glass BSDF or custom refraction shader

## Conversion Process

### Step 1: Set Surface Type
1. Set PBR Master Surface Type to Transparent

### Step 2: Map Parameters
| Blender Input | Unity Input | Notes |
|--------------|-------------|-------|
| Color | Base Color | Tint color |
| IOR | Refraction | Index of Refraction (1.45 for glass) |
| Roughness | Smoothness | Invert for frosted effect |

### Step 3: IOR Handling
- IOR is difficult in standard ShaderGraph
- Use Transparent surface mode with refraction approximation

## Compatibility: 60%

## Limitations
- True refraction requires screen-space calculations
- IOR-based bending not directly supported
- For accurate glass: use custom shader or baked texture
