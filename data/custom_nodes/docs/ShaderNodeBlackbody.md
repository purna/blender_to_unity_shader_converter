# Blender to Unity: ShaderNodeBlackbody Conversion Guide

## Conversion Type: 1 (Direct Mapping)

## Overview
- **Blender Node**: `ShaderNodeBlackbody`
- **Unity ShaderGraph Equivalent**: `Blackbody` (Built-in Node!)
- **Category**: Input / Color
- **Compatibility**: 95% (Direct mapping)

This document provides a complete guide for recreating the functionality of Blender's `ShaderNodeBlackbody` in Unity.

## 1. Good News!
Unity ShaderGraph **DOES have a built-in Blackbody node**! This makes conversion straightforward - no custom code required.

## 2. Unity Blackbody Node

### Node Location
In Unity ShaderGraph, find the Blackbody node under: **Input → Blackbody**

### Ports
| Name | Direction | Type | Description |
|:------------ |:-------------|:-----|:---|
| Temperature | Input | Float | Temperature or temperature map in Kelvin |
| Out | Output | Vector3 | Color in linear RGB space |

### Algorithm
The Unity Blackbody node uses calculations based on data from Mitchell Charity. It outputs color in linear RGB space using a D65 whitepoint and CIE 1964 10 degree color space.

For more information, see [What color is a blackbody?](http://www.vendian.org/mncharity/dir3/blackbody/)

### Example HLSL (for reference)
```hlsl
void Unity_Blackbody_float(float Temperature, out float3 Out)
{
    float3 color = float3(255.0, 255.0, 255.0);
    color.x = 56100000. * pow(Temperature,(-3.0 / 2.0)) + 148.0;
    color.y = 100.04 * log(Temperature) - 623.6;
    if (Temperature > 6500.0) color.y = 35200000.0 * pow(Temperature,(-3.0 / 2.0)) + 184.0;
    color.z = 194.18 * log(Temperature) - 1448.6;
    color = clamp(color, 0.0, 255.0)/255.0;
    if (Temperature < 1000.0) color *= Temperature/1000.0;
    Out = color;
}
```

## 3. Step-by-Step Conversion

### Blender Setup
1. In Blender, select the Blackbody node
2. Set the Temperature (typically 6500K for daylight, 2700K for warm light)

### Unity Setup
1. In ShaderGraph, add a **Blackbody** node (Input category)
2. Connect a Float property or value to Temperature
3. Connect the output to your desired input (Emission, Base Color, etc.)

### Visual Graph Layout
```
[Float Property ("Temperature")] --(Out)--> [Blackbody Node].[Temperature]
                                        [Blackbody Node].[Out] --(Out)--> [PBR Master Node].[Emission]
```

## 4. Common Temperature Values
| Effect | Kelvin |
|:-------|:-------|
| Candle flame | 1800K |
| Warm tungsten | 2700K |
| Halogen | 3200K |
| Fluorescent | 4000K |
| Daylight | 5500K |
| Overcast sky | 6500K |
| Clear blue sky | 10000K+ |

## 5. Example
See [`Color/Gamma.shadersubgraph`](../../examples/Color/Gamma.shadersubgraph) for a similar color conversion node example.
