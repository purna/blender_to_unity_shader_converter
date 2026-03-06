# ShaderNodeColorRamp - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Color
- **Compatibility**: 75%

## Blender Node Description
Maps grayscale [0-1] input to color gradient. Supports multiple color stops with easing.

## Unity Equivalent
- **Primary**: Sample Gradient node
- **Implementation**: Gradient property with color stops

## Conversion Process

### Step 1: Create Gradient Property
- Create Gradient property in Unity
- Add color stops matching Blender ramp

### Step 2: Connect to Sample Gradient
- Connect grayscale input to Sample Gradient Time input

### Step 3: Output Color
- Connect output to target

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Fac | Float | Time | Direct |
| Color_Ramp | Gradient | Gradient | Create property |

## Compatibility Notes
- Interpolation differs slightly
- 75% compatible - good approximation

## Limitations
- Complex curves require custom function
- Exact interpolation differs
- Easing options limited
