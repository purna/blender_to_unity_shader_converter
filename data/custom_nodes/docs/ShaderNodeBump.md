# ShaderNodeBump - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Vector
- **Compatibility**: 75%

## Blender Node Description
Converts height to normal using finite differences. Creates normal map from grayscale height input.

## Unity Equivalent
- **Primary**: Normal From Height node
- **Implementation**: Direct height-to-normal conversion

## Conversion Process

### Step 1: Create Normal From Height
- Add Normal From Height node
- Connect height texture to input

### Step 2: Connect to PBR Master
- Connect output to Normal input on PBR Master
- Adjust Scale for strength

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Strength | Float | Scale | Direct |
| Distance | Float | N/A | Not supported |
| Height | Float | Input | Direct |

## Compatibility Notes
- Algorithm differs slightly between engines
- 75% compatible - good approximation

## Limitations
- Exact finite difference calculation varies
- Distance parameter not directly supported
- May need manual adjustment
