# Combine HSV Node

## Overview
The Combine HSV node combines separate Hue, Saturation, and Value components into a single color.

## Blender Node Inputs
- **H**: Hue component (0-1 range, representing 0-360 degrees)
- **S**: Saturation component (0-1 range)
- **V**: Value/Brightness component (0-1 range)

## Blender Node Outputs
- **Color**: Combined color in HSV space (stored as RGB)

## Unity Equivalent

### Primary Option: Custom Calculation
Unity doesn't have a native HSV node. Implement HSV-to-RGB conversion:

### HSV to RGB Formula
```
// Convert HSV to RGB:
// H = hue (0-1), S = saturation (0-1), V = value (0-1)

float h = H * 6.0;
float c = V * S;
float x = c * (1 - abs(fmod(h, 2) - 1));
float m = V - c;

float3 rgb;
float modH = fmod(h, 6);

if (modH < 1) rgb = float3(c, x, 0);
else if (modH < 2) rgb = float3(x, c, 0);
else if (modH < 3) rgb = float3(0, c, x);
else if (modH < 4) rgb = float3(0, x, c);
else if (modH < 5) rgb = float3(x, 0, c);
else rgb = float3(c, 0, x);

rgb += m;
```

## Conversion Strategy

### Using Unity's Built-in Nodes
1. Use **Combine** node to combine R, G, B channels
2. Pre-calculate HSV values externally
3. Use material properties for hue/saturation

### For Dynamic Color Adjustment
Create a custom shader with HSV properties:
```
Properties:
  _Hue ("Hue", Range(0, 1)) = 0
  _Saturation ("Saturation", Range(0, 2)) = 1
  _Value ("Value", Range(0, 2)) = 1

Fragment Shader:
  Apply HSV transformation to base color
```

### Alternative: Color Property
Use Unity's Color property with HDR for hue/saturation:
- Set HDR intensity for value
- Use Color Picker for hue selection

## Compatibility
- **Compatibility**: 40%
- **Notes**: Requires custom shader logic. Basic combinations possible with built-in nodes.

## Additional Resources
- [HSV Color Space Wikipedia](https://en.wikipedia.org/wiki/HSL_and_HSV)
- [Unity Shader Graph Combine Node](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Combine-Node.html)
- [Blender Combine HSV Node](https://docs.blender.org/manual/en/latest/render/shader_nodes/converter/combine_hsv.html)
