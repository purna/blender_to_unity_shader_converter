# Separate HSV Node

## Overview
The Separate HSV node converts a color from HSV (Hue, Saturation, Value) color space into its individual components: Hue, Saturation, and Value.

## Blender Node Inputs
- **Color**: Input color in HSV space (RGBA)

## Blender Node Outputs
- **H**: Hue component (0-1 range, representing 0-360 degrees)
- **S**: Saturation component (0-1 range)
- **V**: Value/Brightness component (0-1 range)

## Unity Equivalent

### Primary Option: Split Node + Custom Calculation
Unity doesn't have a native HSV node, but you can extract components using math:

1. Use a **Split** node to extract R, G, B (which hold H, S, V in Blender)
2. Implement HSV-to-RGB conversion manually

### HSV to RGB Formula
```
// Convert HSV to RGB in shader:
// H = hue (0-1), S = saturation (0-1), V = value (0-1)

float3 RGB;
float h = H * 6;
float c = V * S;
float x = c * (1 - abs(fmod(h, 2) - 1));
float m = V - c;

if (h < 1) RGB = float3(c, x, 0);
else if (h < 2) RGB = float3(x, c, 0);
else if (h < 3) RGB = float3(0, c, x);
else if (h < 4) RGB = float3(0, x, c);
else if (h < 5) RGB = float3(x, 0, c);
else RGB = float3(c, 0, x);

RGB += m;
```

## Conversion Strategy

### For Color Adjustment Effects
1. Use Unity's **Color** node for hue/saturation adjustments
2. Use **Channel Mixer** for advanced color manipulation
3. Use **Replace Color** for hue shifting

### Custom Shader Graph Implementation
Create a custom HSV adjustment node in Shader Graph:
```
1. Add Float properties: Hue, Saturation, Value
2. Add Color input
3. Implement HSV conversion logic
4. Output adjusted color
```

### Using Post-Processing
For complex HSV adjustments, use Unity's Post-Processing Stack:
- Color Adjustments effect
- Tonemapping

## Compatibility
- **Compatibility**: 40%
- **Notes**: Requires custom shader logic. Basic color grading available via built-in nodes.

## Additional Resources
- [HSV Color Space Wikipedia](https://en.wikipedia.org/wiki/HSL_and_HSV)
- [Unity Shader Graph Manual](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html)
- [Blender Separate HSV Node](https://docs.blender.org/manual/en/latest/render/shader_nodes/converter/separate_hsv.html)
