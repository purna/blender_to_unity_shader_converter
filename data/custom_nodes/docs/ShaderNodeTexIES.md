# ShaderNodeTexIES - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Texture
- **Compatibility**: 70%

## Blender Node Description
IES Texture - loads IES light profile files for realistic lighting falloff.

## Unity Equivalent
- **Primary**: Light Cookies / Custom Function
- **Implementation**: Use Unity's cookie system or custom HLSL

## Conversion Process

### Step 1: Import IES File
- Import IES file to Unity as light cookie
- Use with Light component

### Step 2: Apply as Cookie
- Apply to point/spot light
- Use for realistic falloff

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Vector | Vector | UV | Direct |
| Strength | Float | Intensity | Direct |

## Compatibility Notes
- 70% compatible - requires light setup
- IES not directly supported in ShaderGraph

## Limitations
- Requires manual Unity setup
- Not usable as texture in shaders
