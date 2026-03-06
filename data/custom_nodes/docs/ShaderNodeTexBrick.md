# ShaderNodeTexBrick - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Texture
- **Compatibility**: 60%

## Blender Node Description
Brick texture - procedural brick pattern with customizable brick size, mortar, offset, and colors.

## Unity Equivalent
- **Primary**: Tiling and Offset + Custom Function
- **Implementation**: Use Unity's procedural nodes with custom tiling

## Conversion Process

### Step 1: Create Tiling and Offset
- Use Tiling and Offset node
- Set brick pattern scale

### Step 2: Create Gradient / Step Node
- Use gradient nodes to create brick pattern
- Use step node for mortar separation

### Step 3: Combine Colors
- Use color nodes for brick and mortar colors
- Mix using the mortar mask

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Color1 | Color | Base Color | Direct |
| Color2 | Color | Brick Color | Direct |
| Mortar | Color | Mortar Color | Direct |
| Scale | Float | Tiling | Direct |
| Brick Width | Float | Width | Tiling |
| Brick Height | Float | Height | Tiling |
| Mortar Width | Float | Gap | Partial |
| Offset | Float | Offset | Partial |
| Squash | Float | Squash | Not supported |

## Compatibility Notes
- 60% compatible - requires custom node construction
- Some brick parameters not directly supported

## Limitations
- Complex brick patterns require custom HLSL
- Squash factor not available
- Offset frequency limited
