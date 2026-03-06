# ShaderNodeTexMagic - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Texture
- **Compatibility**: 30%

## Blender Node Description
Magic Texture - procedural chaotic pattern based on iterated trigonometric functions.

## Unity Equivalent
- **Primary**: Custom Function
- **Implementation**: Requires custom HLSL implementation

## Conversion Process

### Step 1: Create Custom Function
- Create Custom Function node
- Write HLSL for magic pattern

### Step 2: Configure Parameters
- Add depth/warping parameters
- Connect UV input

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Vector | Vector | UV | Direct |
| Scale | Float | Scale | Direct |
| Distortion | Float | Distortion | Direct |
| Depth | Integer | Iterations | Direct |

## Compatibility Notes
- 30% compatible - requires custom code
- No built-in equivalent

## Limitations
- Requires custom HLSL implementation
- Complex to replicate exactly
