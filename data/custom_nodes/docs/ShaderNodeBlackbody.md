# ShaderNodeBlackbody

## Overview
| Property | Value |
|----------|-------|
| **Source** | Blender Cycles/Eevee |
| **Target** | Unity URP/HDRP |
| **Compatibility** | 85% |
| **Category** | Input |

## Summary
Temperature color from blackbody radiation - physics-based color conversion from Kelvin temperature to RGB.

## Unity Equivalent
**Color lookup** - hardcoded RGB table or custom calculation

## Conversion Process

### Step 1: Input Temperature
- **Blender Input**: Temperature (Float, Kelvin)
- **Unity Output**: Float value
- **Description**: Read temperature value (typically 1000K-10000K)

### Step 2: Calculate/lookup RGB
- **Blender Input**: Kelvin temperature
- **Unity Output**: Color (Vector3)
- **Description**: Convert temperature to RGB using formula or lookup

### Step 3: Output Color
- **Blender Input**: Calculated color
- **Unity Output**: Color output
- **Description**: Connect to material color input

## Parameters
| Blender | Description |
|---------|-------------|
| Temperature | Temperature in Kelvin (1000K-10000K) |

## Temperature Range
| Temperature | Color |
|------------|-------|
| 500K | Red |
| 1000K | Orange |
| 4000K | White |
| 6600K | Daylight |
| 10000K | Blue-white |

## Compatibility
- **Fully Compatible**: Standard temperature range (1000K-10000K)
- **Partially Compatible**: Extreme temperatures
- **Incompatible**: None

## Implementation
- Use Kelvin to RGB formula
- Or use a look-up texture
- Create custom function node in ShaderGraph

## Limitations
- Requires custom implementation (no native Blackbody node)
- Formula approximation may differ slightly from Blender
