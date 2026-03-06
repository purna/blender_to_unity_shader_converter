# ShaderNodeTexChecker - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Texture
- **Compatibility**: 70%

## Blender Node Description
Checker texture - procedural checkerboard pattern with two colors.

## Unity Equivalent
- **Primary**: Gradient (Linear) + Step + Tiling and Offset
- **Implementation**: Construct checker pattern using basic nodes

## Conversion Process

### Step 1: Create Tiling
- Use Tiling and Offset node
- Set scale for checker size

### Step 2: Create Gradient
- Use Gradient node (Linear)
- Scale UV to create repeating pattern

### Step 3: Apply Step
- Use Step node to create sharp edges
- Set threshold at 0.5

### Step 4: Mix Colors
- Use Lerp node to mix two colors
- Use checker pattern as alpha

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Color1 | Color | Color A | Direct |
| Color2 | Color | Color B | Direct |
| Scale | Float | Tiling | Direct |

## Compatibility Notes
- 70% compatible - requires node construction
- Simple checker pattern can be replicated

## Limitations
- Only works for 2-color checker
- Complex checker patterns not supported
