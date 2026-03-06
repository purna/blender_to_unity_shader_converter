# ShaderNodeColorRamp

## Conversion Type: 3 (Multi-Node Conversion)

## Overview
- **Blender Node**: ShaderNodeColorRamp
- **Category**: Converter
- **Compatibility**: 80%

## Unity Equivalent
- **Primary**: Sample Gradient node (simplified)
- **Full**: Custom Function with color stops

## Conversion Process

### Step 1: Sample Gradient
- **Description**: Map input factor to gradient
- **Blender Input**: Factor (0-1)
- **Unity Output**: Color from gradient

### Step 2: Handle Color Stops
- **Description**: Create gradient with multiple colors
- **Blender Input**: Color stops array
- **Unity Output**: Gradient definition

## Blender to Unity Mapping

| Blender Parameter | Unity Implementation | Compatibility |
|-------------------|---------------------|---------------|
| Fac | Sample Gradient (Input) | 100% |
| Color Ramp | Gradient | 80% |

## Visual Graph Layout

```
// Simple Color Ramp (2 colors)
[Float: 0-1] ──> [Sample Gradient] ──> [Color Output]
                       ^
                       │
                 [Gradient: Color A to B]

// Multi-stop Color Ramp (requires Custom Function)
[Float: 0-1] ──> [Custom Function: ColorRamp] ──> [Color Output]
```

## Pseudocode for Conversion Logic

```python
def convert_colorramp_node(blender_node):
    """
    Converts Blender ShaderNodeColorRamp to Unity ShaderGraph.
    Multi-node conversion - gradient sampling with color stops.
    """
    # 1. Get inputs
    factor_input = get_input_connection(blender_node.inputs["Fac"])
    
    # Get color stops
    color_stops = blender_node.color_ramp.elements  # List of (position, color)
    
    # 2. Sort stops by position
    sorted_stops = sorted(color_stops, key=lambda s: s.position)
    
    if len(sorted_stops) == 2 and sorted_stops[0].position == 0.0 and sorted_stops[1].position == 1.0:
        # Simple gradient - use Unity's Sample Gradient node
        gradient_node = create_shadergraph_node("Sample Gradient")
        
        # Create gradient with two colors
        gradient = create_gradient(
            colors=[sorted_stops[0].color, sorted_stops[1].color],
            positions=[0.0, 1.0]
        )
        gradient_node.set_property("Gradient", gradient)
        
        # Connect factor
        if factor_input:
            connect_nodes(factor_input, gradient_node, "Time")
        else:
            gradient_node.set_input("Time", blender_node.inputs["Fac"].default_value)
        
        return gradient_node.outputs["Out"]
    
    else:
        # Multi-stop gradient - need custom function
        # Build HLSL code for the color ramp
        colors = [stop.color for stop in sorted_stops]
        positions = [stop.position for stop in sorted_stops]
        
        func_body = _build_colorramp_hsl(colors, positions)
        
        custom_func = create_shadergraph_node("Custom Function", {
            "name": "color_ramp",
            "body": func_body
        })
        
        if factor_input:
            connect_nodes(factor_input, custom_func, "In")
        else:
            custom_func.set_input("In", blender_node.inputs["Fac"].default_value)
        
        return custom_func.outputs["Out"]


def _build_colorramp_hsl(colors, positions):
    """Build HLSL code for multi-stop color ramp"""
    num_stops = len(colors)
    
    # Initialize arrays
    color_array = ", ".join([f"float4({c[0]}, {c[1]}, {c[2]}, 1.0)" for c in colors])
    pos_array = ", ".join([str(p) for p in positions])
    
    hls = f"""
int numStops = {num_stops};
float4 colors[{num_stops}] = {{ {color_array} }};
float stops[{num_stops}] = {{ {pos_array} }};

float t = saturate(In);

for (int i = 0; i < numStops - 1; i++) {{
    if (t >= stops[i] && t <= stops[i+1]) {{
        float localT = (t - stops[i]) / (stops[i+1] - stops[i]);
        return lerp(colors[i], colors[i+1], localT);
    }}
}}

return colors[numStops-1];
"""
    return hls
```

## Compatibility Notes
- 80% compatible
- Simple gradients work directly
- Complex multi-stop gradients require custom function

## Limitations
- Alpha handling differs
- Interpolation modes (Linear, Bezier, Cardinal) may differ
