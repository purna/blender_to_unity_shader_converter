# ShaderNodeMixRGB

## Conversion Type: 3 (Multi-Node Conversion)

## Overview
- **Blender Node**: ShaderNodeMixRGB
- **Category**: Color
- **Compatibility**: 90%

## Unity Equivalent
Multiple nodes required depending on blend mode:
- **Simple Mix**: Lerp node
- **Darken/Lighten**: Min/Max nodes  
- **Multiply**: Multiply node
- **Screen/Add**: Add/Subtract with custom math
- **Overlay/Soft Light**: Custom Function node

## Conversion Process

### Step 1: Select Blend Mode
- **Description**: Choose the appropriate blend operation
- **Blender Input**: Color1, Color2, Factor, Mode
- **Unity Output**: Blended color

### Step 2: Apply Blend
- **Description**: Use appropriate Unity node for the blend mode
- **Blender Input**: Blend mode selection
- **Unity Output**: Blended result

## Blender to Unity Mapping

| Blender Mode | Unity Implementation | Compatibility |
|--------------|---------------------|---------------|
| Mix | Lerp | 100% |
| Darken | Min | 100% |
| Multiply | Multiply | 100% |
| Lighten | Max | 100% |
| Screen | Screen formula | 90% |
| Add | Add | 100% |
| Overlay | Custom function | 80% |
| Soft Light | Custom function | 80% |

## Build Instructions

1. Identify blend mode in Blender
2. Create appropriate Unity node (Lerp, Add, Multiply, etc.)
3. Connect colors and factor
4. For Overlay/Soft Light, use Custom Function node

## Visual Graph Layout

```
// Mix Blend Mode (simplest)
[Color1] ──> [Lerp] <─ [Factor: 0.5] ──> [Output]
              ^
              │
[Color2] ─────┘

// Multiply Blend Mode
[Color1] ──> [Multiply] ──> [Output]
              ^
              │
[Color2] ─────┘

// Screen Blend Mode (1 - (1-A) * (1-B))
[Color1] ──> [One Minus] ──┐
                          ├─> [Multiply] ──> [One Minus] ──> [Output]
[Color2] ──> [One Minus] ──┘

// Overlay: Multiply or Screen depending on base
[Color1] ──> [Lerp] <──────────────────────────────────┐
              ^                                       │
              │                                       V
[Color2] ──> [Branch] ──> [Equal: 0.5] ──> [Split] ──> [Output]
              ^                    ^             ^
              │                    │             │
              └────────────────────┴─────────────┘
         (Actually requires Custom Function for exact match)
```

## Pseudocode for Conversion Logic

```python
def convert_mix_rgb_node(blender_node):
    """
    Converts Blender ShaderNodeMixRGB to Unity ShaderGraph nodes.
    This is a multi-node conversion - different blend modes require different Unity nodes.
    """
    blend_mode = blender_node.blend_type  # Mix, Darken, Multiply, Lighten, Screen, Add, Overlay, Soft Light
    factor_input = get_input_connection(blender_node.inputs["Fac"])
    color1_input = get_input_connection(blender_node.inputs[0])  # Color1
    color2_input = get_input_connection(blender_node.inputs[1])  # Color2
    
    # Get default values if inputs not connected
    color1_val = color1_input or blender_node.inputs[0].default_value
    color2_val = color2_input or blender_node.inputs[1].default_value
    factor_val = factor_input or blender_node.inputs["Fac"].default_value
    
    if blend_mode == "MIX":
        # Simple Lerp: lerp(Color1, Color2, Factor)
        lerp_node = create_shadergraph_node("Lerp")
        if color1_input:
            connect_nodes(color1_input, lerp_node, "A")
        if color2_input:
            connect_nodes(color2_input, lerp_node, "B")
        if factor_input:
            connect_nodes(factor_input, lerp_node, "T")
        else:
            lerp_node.set_input("T", factor_val)
        return lerp_node
    
    elif blend_mode == "DARKEN":
        # min(Color1, Color2)
        min_node = create_shadergraph_node("Min")
        _connect_color_input(color1_input, color1_val, min_node, "A")
        _connect_color_input(color2_input, color2_val, min_node, "B")
        return min_node
    
    elif blend_mode == "MULTIPLY":
        # Color1 * Color2
        multiply_node = create_shadergraph_node("Multiply")
        _connect_color_input(color1_input, color1_val, multiply_node, "A")
        _connect_color_input(color2_input, color2_val, multiply_node, "B")
        return multiply_node
    
    elif blend_mode == "LIGHTEN":
        # max(Color1, Color2)
        max_node = create_shadergraph_node("Max")
        _connect_color_input(color1_input, color1_val, max_node, "A")
        _connect_color_input(color2_input, color2_val, max_node, "B")
        return max_node
    
    elif blend_mode == "SCREEN":
        # 1 - (1 - Color1) * (1 - Color2) = Color1 + Color2 - Color1 * Color2
        # Implementation requires multiple nodes
        return _create_screen_blend(color1_input, color1_val, color2_input, color2_val)
    
    elif blend_mode == "ADD":
        # Color1 + Color2 (optionally with factor)
        add_node = create_shadergraph_node("Add")
        _connect_color_input(color1_input, color1_val, add_node, "A")
        _connect_color_input(color2_input, color2_val, add_node, "B")
        return add_node
    
    elif blend_mode in ["OVERLAY", "SOFT_LIGHT"]:
        # These require custom function for exact match
        # Overlay: A < 0.5 ? 2*A*B : 1-2*(1-A)*(1-B)
        custom_func = create_shadergraph_node("Custom Function", {
            "name": blend_mode.lower(),
            "body": _get_overlay_softlight_body(blend_mode)
        })
        _connect_color_input(color1_input, color1_val, custom_func, "A")
        _connect_color_input(color2_input, color2_val, custom_func, "B")
        return custom_func
    
    else:
        # Default to Mix/Lerp
        return _create_lerp(color1_input, color1_val, color2_input, color2_val, factor_val)


def _create_screen_blend(c1, c1_val, c2, c2_val):
    """Create screen blend: 1 - (1-A) * (1-B)"""
    # This is complex in ShaderGraph, would need multiple nodes
    # For implementation, create Custom Function node
    screen_func = create_shadergraph_node("Custom Function", {
        "name": "screen",
        "body": "return 1.0 - (1.0 - A) * (1.0 - B);"
    })
    _connect_color_input(c1, c1_val, screen_func, "A")
    _connect_color_input(c2, c2_val, screen_func, "B")
    return screen_func


def _connect_color_input(node_input, default_val, target_node, port):
    """Helper to connect color input or use default value"""
    if node_input:
        connect_nodes(node_input, target_node, port)
    else:
        target_node.set_input(port, default_val)


def _get_overlay_softlight_body(blend_mode):
    """Get shader code for Overlay or Soft Light"""
    if blend_mode == "OVERLAY":
        return """
float4 Overlay(float4 A, float4 B) {
    return A < 0.5 ? 2*A*B : 1-2*(1-A)*(1-B);
}
return Overlay(A, B);
"""
    else:  # SOFT_LIGHT
        return """
float4 SoftLight(float4 A, float4 B) {
    // Approximation of Soft Light
    float4 result = A;
    for(int i=0; i<4; i++) {
        if (B[i] < 0.5) {
            result[i] = A[i] - (1 - 2*B[i])*A[i]*(1-A[i]);
        } else {
            float d = (A[i] <= 0.25) ? ((16*A[i]-12)*A[i]+4)*A[i] : sqrt(A[i]);
            result[i] = A[i] + (2*B[i]-1)*(d-A[i]);
        }
    }
    return result;
}
return SoftLight(A, B);
"""
```

## Notes
- Most blend modes map directly
- Overlay and Soft Light require custom functions for exact match
- 10% loss due to complex blend mode differences
- Factor input can modify blend in some modes
