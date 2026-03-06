# ShaderNodeGamma - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Color
- **Compatibility**: 90%

## Blender Node Description
Gamma correction. Applies power curve to color.

## Unity Equivalent
- **Primary**: Power node
- **Implementation**: Formula: pow(Color, 1/Gamma)

## Conversion Process

### Step 1: Create Power Node
- Add Power node in Unity

### Step 2: Connect Color
- Connect Color to Power input

### Step 3: Set Exponent
- Set exponent to 1/Gamma

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Color | Vector4 | Input | Direct |
| Gamma | Float | Exponent | 1/Gamma |

## Compatibility Notes
- 90% compatible
- Formula: output = input ^ (1/gamma)

## Limitations
- None significant
