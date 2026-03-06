# ShaderNodeCurveFloat - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Utility
- **Compatibility**: 50%

## Blender Node Description
Applies arbitrary curve to float value. Maps input through a spline curve.

## Unity Equivalent
- **Primary**: Curve node
- **Implementation**: Approximation with linear interpolation

## Conversion Process

### Step 1: Create Curve Property
- Create Curve property in Unity

### Step 2: Connect Value
- Connect value through curve node

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Value | Float | Input | Direct |
| Curve | Curve | Curve property | Approximate |

## Compatibility Notes
- 50% compatible - complex curves difficult

## Limitations
- Linear approximation for complex curves
- Spline evaluation differs
