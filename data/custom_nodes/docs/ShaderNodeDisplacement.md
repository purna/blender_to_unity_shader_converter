# ShaderNodeDisplacement - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Vector
- **Compatibility**: 60%

## Blender Node Description
Vertex displacement from heightmap. Displaces mesh vertices along normals.

## Unity Equivalent
- **Primary**: Vertex Offset
- **Implementation**: Requires tessellation or displacement pass

## Conversion Process

### Step 1: Choose Approach
- Option 1: Geometry/Vertex Displacement (advanced)
- Option 2: Parallax occlusion mapping (approximation)
- Option 3: Tessellation shader (if available)

### Step 2: Implement Displacement
- Use Vertex Position node with displacement

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Height | Float | Height | Grayscale |
| Midlevel | Float | N/A | Not supported |
| Scale | Float | Scale | Direct |
| Normal | Normal | Normal | Direct |

## Compatibility Notes
- 60% compatible
- Standard ShaderGraph doesn't support vertex modification

## Limitations
- True displacement requires vertex processing
- ShaderGraph alone cannot modify geometry
- Use parallax as visual approximation
