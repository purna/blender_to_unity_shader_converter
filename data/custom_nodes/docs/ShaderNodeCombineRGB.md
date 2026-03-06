# ShaderNodeCombineRGB - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Vector
- **Compatibility**: 100%

## Blender Node Description
Combines R, G, B float values into a single color output.

## Unity Equivalent
- **Primary**: Combine (Vector) node
- **Implementation**: 1:1 direct mapping

## Conversion Process

### Step 1: Create Combine Node
- Add Combine node in Unity

### Step 2: Connect Channels
- Connect R, G, B to respective inputs

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| R | Float | R | Direct |
| G | Float | G | Direct |
| B | Float | B | Direct |

## Compatibility Notes
- 100% compatible - direct 1:1 mapping
- No limitations

## Limitations
- None
