# ShaderNodeTexGradient - Research & Action Plan

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Texture
- **Compatibility**: 100%

## Blender Node Description
Gradient texture - procedural gradient patterns (Linear, Radial, Quadratic, Spherical, Quadratic Sphere, Diagonal).

## Unity Equivalent
- **Primary**: Gradient Node
- **Implementation**: Direct 1:1 mapping

## Conversion Process

### Step 1: Create Gradient Node
- Add Gradient node in Unity ShaderGraph

### Step 2: Configure Type
- Linear: Use Linear gradient
- Radial: Use Radial gradient
- Quadratic: Custom (not available)

### Step 3: Connect UV
- Connect UV to Gradient input

## Parameters
| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Vector | Vector | UV | Direct |
| Gradient Type | Enum | Gradient Type | Partial |

## Compatibility Notes
- 100% compatible for basic gradients
- Some gradient types require custom nodes

## Limitations
- Quadratic/Spherical not directly available
- Diagonal requires custom UV manipulation
