# ShaderNodeTexSky - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Texture
- **Compatibility**: 60%

## Blender Node Description
Sky Texture - procedural atmospheric sky with sun position, turbidity, and ground albedo.

## Unity Equivalent
- **Primary**: HDRI Environment
- **Implementation**: Use Unity's sky system

## Conversion Process

### Step 1: Create Sky
- Use Unity's procedural sky
- Or import sky HDRI

### Step 2: Configure Sun
- Set sun direction
- Adjust atmospheric settings

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Vector | Vector | Direction | Direct |
| Sky Model | Enum | Sky Type | Partial |
| Sun Position | Vector | Sun Direction | Direct |
| Turbidity | Float | Atmosphere | Partial |
| Ground Albedo | Color | Ground | Partial |

## Compatibility Notes
- 60% compatible - sky system differs
- Procedural sky different

## Limitations
- Procedural sky different implementation
- Limited atmospheric control
