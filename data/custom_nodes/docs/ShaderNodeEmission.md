# ShaderNodeEmission - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Shader
- **Compatibility**: 85%

## Blender Node Description
Self-illuminating material. Makes surface emit light.

## Unity Equivalent
- **Primary**: Emission on PBR Master
- **Implementation**: Direct mapping with Color × Strength

## Conversion Process

### Step 1: Create PBR Master
- Use Lit material with Emission

### Step 2: Connect Emission
- Connect Color × Strength to Emission input

### Step 3: Enable HDR
- Enable HDR color property for values > 1

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Color | Color | Emission Color | Direct |
| Strength | Float | Multiply | Color × Strength |

## Compatibility Notes
- 85% compatible
- Blender emission affects global illumination

## Limitations
- Unity emission is mostly visual except in baked GI
- No bloom auto-enable
