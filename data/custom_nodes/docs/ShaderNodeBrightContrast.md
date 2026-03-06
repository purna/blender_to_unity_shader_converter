# ShaderNodeBrightContrast

## Overview
| Property | Value |
|----------|-------|
| **Source** | Blender Cycles/Eevee |
| **Target** | Unity URP/HDRP |
| **Compatibility** | 80% |
| **Category** | Color |
| **Complexity** | Low-Medium |

## Summary
Adjusts color brightness and contrast using simple math formulas.

## Unity Equivalent
**Brightness-Contrast** node or custom math nodes

## Conversion Process

### Step 1: Apply Brightness
- **Blender Input**: Color, Bright
- **Unity Output**: Add node result
- **Description**: Formula: output = input + bright_value
- **Formula**: Color + Brightness

### Step 2: Apply Contrast
- **Blender Input**: Brightened color, Contrast
- **Unity Output**: Multiply result
- **Description**: Formula: (Color - 0.5) * Contrast + 0.5

### Step 3: Output Result
- **Blender Input**: Final adjusted color
- **Unity Output**: Color output
- **Description**: Connect to material

## Parameters
| Blender | Description |
|---------|-------------|
| Color | Input color to adjust |
| Bright | Brightness value (-1 to +1) |
| Contrast | Contrast multiplier (0.5 to 2.0) |

## Formulas
| Operation | Formula |
|-----------|---------|
| Brightness | output = input + bright_value |
| Contrast | output = (input - 0.5) * contrast + 0.5 |

## Unity Implementation
```
[Color] → [Add(Brightness)] → [Multiply(Contrast)] → [Add(0.5)] → [Output]
```

## Compatibility
- **Fully Compatible**: Basic brightness/contrast adjustments
- **Partially Compatible**: Extreme values (may clamp differently)
- **Incompatible**: None

## Limitations
- Minor non-linear differences in how extreme values are clamped
- May need manual tuning for exact match
