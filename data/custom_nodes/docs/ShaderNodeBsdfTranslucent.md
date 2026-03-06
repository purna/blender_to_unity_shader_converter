# ShaderNodeBsdfTranslucent - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Shader
- **Compatibility**: 40%

## Blender Node Description
Translucent shader - light passes through surfaces (paper, leaves, cloth). Models subsurface scattering for thin materials.

## Unity Equivalent
- **Primary**: Transparent PBR with approximation
- **Fallback**: Custom shader for SSS

## Conversion Process

### Step 1: Set Surface Type
- Create PBR Master node
- Set Surface Type to Transparent

### Step 2: Connect Color
- Connect Color to Base Color input
- Adjust alpha for translucency effect

### Step 3: Normal (Optional)
- Connect Normal input if provided

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Color | Color | Base Color + Alpha | Direct with alpha |
| Normal | Normal | Normal | Direct |

## Compatibility Notes
- No native translucency in ShaderGraph
- Light penetration not truly supported
- Approximation only

## Limitations
- Light penetration not supported
- Custom shader required for accurate results
- No backlight transmission
