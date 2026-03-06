# ShaderNodeCombineXYZ - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Vector
- **Compatibility**: 100%

## Blender Node Description
Combines X, Y, Z float values into a single vector output.

## Unity Equivalent
- **Primary**: Combine (Vector) node
- **Implementation**: 1:1 direct mapping

## Conversion Process

### Step 1: Create Combine Node
- Add Combine node in Unity

### Step 2: Connect Channels
- Connect X, Y, Z to respective inputs

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| X | Float | X | Direct |
| Y | Float | Y | Direct |
| Z | Float | Z | Direct |

## Compatibility Notes
- 100% compatible - direct 1:1 mapping
- No limitations
