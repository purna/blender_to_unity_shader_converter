# ShaderNodeTexStucci - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Texture
- **Compatibility**: 30%

## Blender Node Description
Stucci Texture - procedural wall-like noise pattern with wood or cement appearance.

## Unity Equivalent
- **Primary**: Custom Function
- **Implementation**: Requires custom HLSL

## Conversion Process

### Step 1: Create Custom Function
- Add Custom Function node
- Write HLSL for Stucci pattern

### Step 2: Configure Parameters
- Set scale and distortion
- Connect UV input

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Vector | Vector | UV | Direct |
| Scale | Float | Scale | Direct |
| Size | Float | Scale | Direct |
| Distortion | Float | Distortion | Direct |
| Texture Type | Enum | Type | Not supported |

## Compatibility Notes
- 30% compatible - requires custom code
- No built-in equivalent

## Limitations
- Requires custom HLSL implementation
- Texture types not available
