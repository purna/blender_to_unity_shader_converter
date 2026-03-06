# ShaderNodeTexWave - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Texture
- **Compatibility**: 60%

## Blender Node Description
Wave Texture - procedural banded wave pattern with distortion and rings.

## Unity Equivalent
- **Primary**: Gradient (Linear/Radial) + Sine
- **Implementation**: Construct with basic nodes

## Conversion Process

### Step 1: Create Gradient
- Use Gradient node (Linear or Radial)
- Set appropriate orientation

### Step 2: Add Sine Wave
- Use Sine Math node
- Apply to gradient output

### Step 3: Add Distortion
- Add noise for distortion
- Use Add node to combine

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Vector | Vector | UV | Direct |
| Scale | Float | Scale | Direct |
| Distortion | Float | Distortion | Direct |
| Bands Direction | Enum | Orientation | Direct |
| Rings | Float | Frequency | Direct |

## Compatibility Notes
- 60% compatible - basic wave can be built
- Complex waves require custom nodes

## Limitations
- Different wave algorithm
- Rings direction limited
