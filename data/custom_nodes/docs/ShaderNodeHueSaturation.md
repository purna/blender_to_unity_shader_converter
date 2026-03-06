# ShaderNodeHueSaturation

## Conversion Type: 3 (Multi-Node Conversion)

## Overview
- **Blender Node**: ShaderNodeHueSaturation
- **Category**: Color
- **Compatibility**: 100%
- **Unity Version**: URP/HDRP

## Unity Equivalent
- **Primary**: Hue/Saturation node
- **Implementation**: Multiple Color nodes (HSV conversion)

## Unity Shader Graph Nodes

### Primary Node
| Unity Node | Category | Description |
|------------|----------|-------------|
| [Hue](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Hue-Node.html) | Color | Adjusts hue of input color |

### Supporting Nodes
| Unity Node | Category | Description |
|------------|----------|-------------|
| [RGB to HSV](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/RGB-to-HSV-Node.html) | Color | Converts RGB to HSV color space |
| [HSV to RGB](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/HSV-to-RGB-Node.html) | Color | Converts HSV back to RGB |
| [Split](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Split-Node.html) | Utility | Splits color into channels |
| [Combine](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Combine-Node.html) | Utility | Combines channels into color |
| [Multiply](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Multiply-Node.html) | Math/Basic | Multiplies channels |

## Blender Parameters

| Blender Parameter | Type | Default | Description |
|-------------------|------|---------|-------------|
| Hue | Float | 0.5 | Hue shift (0-1, wraps around) |
| Saturation | Float | 1.0 | Saturation multiplier (0-2) |
| Value | Float | 1.0 | Value/brightness (0-2) |
| Color | Color | 1.0, 1.0, 1.0, 1.0 | Input color |

## Conversion Process

### Step 1: Convert to HSV
- **Description**: Convert RGB to HSV color space
- **Blender Input**: Color
- **Unity Output**: HSV

### Step 2: Apply Hue
- **Description**: Shift hue value
- **Blender Input**: Hue (0-1)
- **Unity Output**: Modified Hue

### Step 3: Apply Saturation
- **Description**: Scale saturation
- **Blender Input**: Saturation (0-2)
- **Unity Output**: Modified Saturation

### Step 4: Apply Value
- **Description**: Scale value/brightness
- **Blender Input**: Value (0-1)
- **Unity Output**: Modified Value

### Step 5: Convert back to RGB
- **Description**: Convert HSV back to RGB
- **Unity Output**: Final Color

## Unity Connections

### Using Unity's Hue Node (Simplified)
```
Blender Socket          Unity Socket          Unity Node
─────────────────────────────────────────────────────────────────
Color           ──►     In                    Hue
                                                    │
Hue             ──►     Hue                   ──────┤
                                                    ▼
                                               Out ──► [Output]
```

### Full HSV Conversion (Complete)
```
Blender Socket          Unity Socket          Unity Node
─────────────────────────────────────────────────────────────────
Color           ──►     In                  RGB to HSV ──► Split
                                                                     │
Saturation      ──►     Multiply (B) ◄─────── G (Saturation) ────────┤
                                                                     │
Value           ──►     Multiply (B) ◄─────── B (Value) ────────────┤
                                                                     │
Hue             ──►     Add to H ─────────── H (Hue) ───────────────┤
                                                                     │
                                                          Combine ◄──┘
                                                              │
                                                              ▼
                                                        HSV to RGB
                                                              │
                                                              ▼
                                                        Out ──► [Output]
```

## Unity Parameters

| Unity Property | Type | Default | Description |
|----------------|------|---------|-------------|
| In | Vector4 | 0 | Input color |
| Hue | Float | 0 | Hue shift in degrees (0-360) |
| Saturation | Float | 1 | Saturation multiplier |
| Value | Float | 1 | Value/brightness multiplier |

## Visual Graph Layout

```
// Hue Saturation in Unity (requires HSV conversion)
[Color] ──> [RGB to HSV] ──> [Hue Shift] ──> [Saturation Scale] ──> [Value Scale] ──> [HSV to RGB] ──> [Output]

// Using Unity's Hue node (if available)
[Color] ──> [Hue] ──> [Output]
              ^
              │
[Hue: 0-1] ───┘
```

## Pseudocode for Conversion Logic

```python
def convert_huesaturation_node(blender_node):
    """
    Converts Blender ShaderNodeHueSaturation to Unity ShaderGraph.
    Multi-node conversion - requires HSV color space conversion.
    """
    # 1. Get inputs
    color_input = get_input_connection(blender_node.inputs["Color"])
    hue_input = get_input_connection(blender_node.inputs["Hue"])
    sat_input = get_input_connection(blender_node.inputs["Saturation"])
    val_input = get_input_connection(blender_node.inputs["Value"])
    
    # Default values
    hue_val = hue_input or blender_node.inputs["Hue"].default_value
    sat_val = sat_input or blender_node.inputs["Saturation"].default_value
    val_val = val_input or blender_node.inputs["Value"].default_value
    
    if color_input is None:
        color_input = create_shadergraph_node("Color", {
            "value": blender_node.inputs["Color"].default_value
        })
    
    # 2. Convert RGB to HSV
    rgb_to_hsv = create_shadergraph_node("RGB to HSV")
    connect_nodes(color_input, rgb_to_hsv, "RGB")
    
    # 3. Apply Hue shift
    # Unity doesn't have direct hue shift - need custom function
    # Hue in Blender is 0-1, wraps around
    
    if hue_val != 0.5:  # 0.5 is neutral in Blender
        hue_offset = hue_val - 0.5  # Convert to offset (-0.5 to 0.5)
        
        # Use Unity's Hue node if available, else custom function
        hue_node = create_shadergraph_node("Hue")
        hue_node.set_property("Hue", hue_offset)
        connect_nodes(rgb_to_hsv.outputs["HSV"], hue_node, "In")
        
        current = hue_node
    else:
        current = rgb_to_hsv
    
    # 4. Apply Saturation
    if sat_val != 1.0:
        # Multiply the S channel
        split = create_shadergraph_node("Split")
        connect_nodes(current.outputs["HSV"], split, "In")
        
        multiply = create_shadergraph_node("Multiply")
        connect_nodes(split.outputs["G"], multiply, "A")  # G = Saturation
        multiply.set_input("B", sat_val)
        
        # Combine back
        combine = create_shadergraph_node("Combine")
        connect_nodes(split.outputs["R"], combine, "R")  # R = Hue
        connect_nodes(multiply.outputs["Out"], combine, "G")  # G = Saturation
        connect_nodes(split.outputs["B"], combine, "B")  # B = Value
        
        current = combine
    
    # 5. Apply Value
    if val_val != 1.0:
        # Multiply the B channel (Value)
        if current.type == "Combine":
            split = create_shadergraph_node("Split")
            connect_nodes(current.outputs["Out"], split, "In")
            
            multiply = create_shadergraph_node("Multiply")
            connect_nodes(split.outputs["B"], multiply, "A")
            multiply.set_input("B", val_val)
            
            combine = create_shadergraph_node("Combine")
            connect_nodes(split.outputs["R"], combine, "R")
            connect_nodes(split.outputs["G"], combine, "G")
            connect_nodes(multiply.outputs["Out"], combine, "B")
            
            current = combine
    
    # 6. Convert back to RGB
    hsv_to_rgb = create_shadergraph_node("HSV to RGB")
    connect_nodes(current.outputs["Out"], hsv_to_rgb, "HSV")
    
    return hsv_to_rgb.outputs["RGB"]
```

## Example Files

| File | Description |
|------|-------------|
| `data/custom_nodes/examples/Color/HueSaturationValue.shadersubgraph` | Unity Shader Graph subgraph |

## Compatibility Notes
- 100% compatible
- Full HSV conversion works but uses multiple nodes
- Unity's Hue node handles basic hue shifting
- For full Blender compatibility, use HSV conversion chain

## Limitations
- Full HSV conversion requires multiple nodes
- May have slight color differences
