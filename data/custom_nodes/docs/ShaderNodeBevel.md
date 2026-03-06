# ShaderNodeBevel

## Overview
| Property | Value |
|----------|-------|
| **Source** | Blender Cycles/Eevee |
| **Target** | Unity URP/HDRP |
| **Compatibility** | 70% |
| **Category** | Input |

## Summary
Bevel edge detection - approximates rounded edges on surfaces.

## Unity Equivalent
**Bevel** node (if available) or Bump mapping/normal offset

## Conversion Process

### Step 1: Connect Normal Input
- **Blender Input**: Normal
- **Unity Output**: Normal input on Bevel/Bump node
- **Description**: Pass through or generate normal data

### Step 2: Set Distance
- **Blender Input**: Distance (bevel radius)
- **Unity Output**: Bevel amount or Bump strength
- **Description**: Configure the bevel radius

### Step 3: Set Samples
- **Blender Input**: Samples (quality)
- **Unity Output**: Quality setting (if available)
- **Description**: Adjust sample count for quality

### Step 4: Output Normal
- **Blender Input**: Bevel calculation
- **Unity Output**: Normal output
- **Description**: Connect to material Normal input

## Parameters
| Blender | Description |
|---------|-------------|
| Normal | Surface normal (optional) |
| Distance | Bevel radius |
| Samples | Number of samples |

## Unity Alternatives
- Bevel node (Utility → Bevel in newer Shader Graph versions)
- Normal From Height with gradient texture
- Bump Node for approximation

## Compatibility
- **Fully Compatible**: Basic bevel effect
- **Partially Compatible**: Complex bevels (may need manual tuning)
- **Incompatible**: Very high sample counts

## Limitations
- Bevel node may not be available in all Shader Graph versions
- Real-time bevel is expensive
- May need approximation with Bump Node
