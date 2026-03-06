# ShaderNodeBrightContrast

## Conversion Type: 3 (Multi-Node Conversion)

## Overview
- **Blender Node**: ShaderNodeBrightContrast
- **Category**: Color
- **Compatibility**: 100%
- **Unity Version**: URP/HDRP
- **Complexity**: Medium

## Unity Equivalent
Multiple math nodes required (Add, Multiply, Subtract, One Minus)

## Unity Shader Graph Nodes

### Primary Nodes
| Unity Node | Category | Description |
|------------|----------|-------------|
| [Add](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Add-Node.html) | Math/Basic | Adds brightness value |
| [Subtract](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Subtract-Node.html) | Math/Basic | Subtracts 0.5 for contrast calculation |
| [Multiply](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/Multiply-Node.html) | Math/Basic | Multiplies for contrast |
| [One Minus](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/One-Minus-Node.html) | Math/Utility | For contrast center adjustment |

## Blender Parameters

| Blender Parameter | Type | Default | Description |
|-------------------|------|---------|-------------|
| Color | Color | 1.0, 1.0, 1.0, 1.0 | Input color to adjust |
| Bright | Float | 0.0 | Brightness value (-1 to +1) |
| Contrast | Float | 0.0 | Contrast multiplier (0.5 to 2.0) |

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

## Formulas

| Operation | Formula |
|-----------|---------|
| Brightness | output = input + bright_value |
| Contrast | output = (input - 0.5) * contrast + 0.5 |

## Unity Connections

### Full Brightness + Contrast
```
Blender Socket          Unity Socket          Unity Node
─────────────────────────────────────────────────────────────────
Color           ──►     A                    Add
Bright         ──►     B                    │
                           │                │
                           ▼                ▼
                      Out ─────►     A    Subtract
                                         │
                           ┌─────────────┘
                           │   0.5 (const)
                           │   │
                           ▼   ▼
                      Out ─────►     A    Multiply
                           │            │
                           │   Contrast │
                           │            │
                           ▼            ▼
                      Out ─────►     A    Add
                                         │
                                         │  0.5 (const)
                                         │
                                         ▼
                                    Out ──► [Output]
```

### Simplified: Only Brightness
```
Blender Socket          Unity Socket          Unity Node
─────────────────────────────────────────────────────────────────
Color           ──►     A                    Add
Bright         ──►     B                    │
                           │                │
                           ▼                ▼
                      Out ───────────► [Output]
```

### Simplified: Only Contrast
```
Blender Socket          Unity Socket          Unity Node
─────────────────────────────────────────────────────────────────
Color           ──►     A                    Subtract
                                         │
                           0.5 (const)  │
                                         │
                                         ▼
                      Out ─────►     A    Multiply
                                         │
                           Contrast     │
                                         │
                                         ▼
                      Out ─────►     A    Add
                                         │
                                         │  0.5 (const)
                                         │
                                         ▼
                                    Out ──► [Output]
```

## Unity Parameters

| Unity Property | Type | Default | Description |
|----------------|------|---------|-------------|
| A | Dynamic | 0 | First input |
| B | Dynamic | 0 | Second input |

## Visual Graph Layout

```
// Full Brightness + Contrast adjustment
[Color] ──> [Add: +Brightness] ──> [Subtract: 0.5] ──> [Multiply: Contrast] ──> [Add: 0.5] ──> [Output]
                            ^                                                    ^
                            │                                                    │
                      [Float: 0.5] ─────────────────────────────────────────────┘

// Simplified: Only Brightness
[Color] ──> [Add] ──> [Output]
              ^
              │
[Float: Brightness]

// Simplified: Only Contrast  
[Color] ──> [Subtract: 0.5] ──> [Multiply] ──> [Add: 0.5] ──> [Output]
                    ^                    ^                  ^
                    │                    │                  │
              [Float: 0.5]        [Float: Contrast]  [Float: 0.5]
```

## Pseudocode for Conversion Logic

```python
def convert_bright_contrast_node(blender_node):
    """
    Converts Blender ShaderNodeBrightContrast to Unity ShaderGraph nodes.
    Multi-node conversion - requires Add, Multiply, Subtract nodes.
    """
    # 1. Get inputs
    color_input = get_input_connection(blender_node.inputs["Color"])
    bright_input = get_input_connection(blender_node.inputs["Bright"])
    contrast_input = get_input_connection(blender_node.inputs["Contrast"])
    
    # Get default values
    bright_value = bright_input or blender_node.inputs["Bright"].default_value
    contrast_value = contrast_input or blender_node.inputs["Contrast"].default_value
    
    # Start with color input
    if color_input:
        current = color_input
    else:
        # Use default color
        color_value = blender_node.inputs["Color"].default_value
        current = create_shadergraph_node("Color", {"value": color_value})
    
    # 2. Apply Brightness: Color + Bright
    if bright_value != 0.0:
        add_node = create_shadergraph_node("Add")
        
        if bright_input:
            # Dynamic brightness
            connect_nodes(current, add_node, "A")
            connect_nodes(bright_input, add_node, "B")
        else:
            # Static brightness - use Add with constant
            connect_nodes(current, add_node, "A")
            add_node.set_input("B", bright_value)
        
        current = add_node
    
    # 3. Apply Contrast: (Color - 0.5) * Contrast + 0.5
    if contrast_value != 1.0:
        # Step 3a: Subtract 0.5
        subtract1 = create_shadergraph_node("Subtract")
        connect_nodes(current, subtract1, "A")
        subtract1.set_input("B", 0.5)
        
        # Step 3b: Multiply by Contrast
        multiply = create_shadergraph_node("Multiply")
        connect_nodes(subtract1, multiply, "A")
        
        if contrast_input:
            connect_nodes(contrast_input, multiply, "B")
        else:
            multiply.set_input("B", contrast_value)
        
        # Step 3c: Add 0.5
        add2 = create_shadergraph_node("Add")
        connect_nodes(multiply, add2, "A")
        add2.set_input("B", 0.5)
        
        current = add2
    
    return current


def convert_brightness_only(color_input, bright_value):
    """Helper for brightness-only adjustment"""
    add_node = create_shadergraph_node("Add")
    connect_nodes(color_input, add_node, "A")
    add_node.set_input("B", bright_value)
    return add_node


def convert_contrast_only(color_input, contrast_value):
    """Helper for contrast-only adjustment"""
    # Subtract 0.5
    subtract1 = create_shadergraph_node("Subtract")
    connect_nodes(color_input, subtract1, "A")
    subtract1.set_input("B", 0.5)
    
    # Multiply by contrast
    multiply = create_shadergraph_node("Multiply")
    connect_nodes(subtract1, multiply, "A")
    multiply.set_input("B", contrast_value)
    
    # Add 0.5
    add2 = create_shadergraph_node("Add")
    connect_nodes(multiply, add2, "A")
    add2.set_input("B", 0.5)
    
    return add2
```

## Example Files

| File | Description |
|------|-------------|
| `data/custom_nodes/examples/Color/BrightContrast.shadersubgraph` | Unity Shader Graph subgraph |

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
- Unity doesn't have a single Bright-Contrast node
