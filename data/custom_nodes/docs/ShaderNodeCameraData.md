# ShaderNodeCameraData - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Input
- **Compatibility**: 0%

## Blender Node Description
Camera information - renderer specific data. Provides view vector, depth, and screen coordinates.

## Unity Equivalent
- **Primary**: View Direction, Screen Position
- **Implementation**: Partial support only

## Conversion Process

### Step 1: View Vector
- Use View Direction node for view vector
- This provides camera-to-surface direction

### Step 2: Screen Coordinates
- Use Screen Position node for screen coordinates
- Note: Format may differ between engines

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| View Vector | Vector | View Direction | Partial |
| View Z Depth | Float | N/A | Not supported |
| Screen Coord | Vector | Screen Position | Partial |

## Compatibility Notes
- Most camera data NOT accessible in ShaderGraph
- 0% compatible - fundamental limitation

## Limitations
- Most camera data not accessible
- View Z Depth not available
- Requires custom shader code for full feature set
- Screen Position format differs
