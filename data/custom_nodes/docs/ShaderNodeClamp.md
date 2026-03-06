# ShaderNodeClamp - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Utility
- **Compatibility**: 100%

## Blender Node Description
Clamps value to range. Direct mathematical operation with minimum and maximum bounds.

## Unity Equivalent
- **Primary**: Clamp node
- **Implementation**: 1:1 direct mapping

## Conversion Process

### Step 1: Create Clamp Node
- Add Clamp node in Unity

### Step 2: Connect Value
- Connect Value input

### Step 3: Set Bounds
- Set Min and Max values

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Value | Float | In | Direct |
| Min | Float | Min | Direct |
| Max | Float | Max | Direct |

## Compatibility Notes
- 100% compatible - direct 1:1 mapping
- No limitations

## Limitations
- None
