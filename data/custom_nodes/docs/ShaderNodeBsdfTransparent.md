# ShaderNodeBsdfTransparent - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Shader
- **Compatibility**: 85%

## Blender Node Description
Simple transparent shader - alpha-based transparency. Passes light through without refraction.

## Unity Equivalent
- **Primary**: Transparent PBR
- **Implementation**: Direct alpha mapping

## Conversion Process

### Step 1: Create PBR Master
- Create PBR Master node
- Set Surface Type to Transparent

### Step 2: Connect Color
- Connect Color to Base Color
- Alpha comes from Color alpha channel

### Step 3: Configure Alpha
- Ensure Color input has alpha value
- Unity handles alpha transparency automatically

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Color | Color | Base Color + Alpha | Direct |

## Compatibility Notes
- Simple transparency - direct mapping
- 85% compatible - very close match

## Limitations
- No refraction
- No complex light interaction
- Alpha sorting may differ
