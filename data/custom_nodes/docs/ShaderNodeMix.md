# ShaderNodeMix

## Conversion Type: 1-1 (Direct Mapping)

## Overview
- **Blender Node**: ShaderNodeMix
- **Category**: Utility
- **Compatibility**: 100%

## Unity Equivalent
- **Primary**: Lerp node (for Mix mode)
- **Other**: Add, Subtract, Multiply nodes for other blend modes

## Conversion Process

### Step 1: Direct Port
- **Description**: Blends two values using Lerp (linear interpolation)
- **Blender Input**: A, B, Factor (0-1)
- **Unity Output**: Blended value

## Blender to Unity Mapping

| Blender Mode | Unity Implementation | Compatibility |
|--------------|---------------------|---------------|
| Mix (Lerp) | Lerp node | 100% |
| Add | Add | 100% |
| Subtract | Subtract | 100% |
| Multiply | Multiply | 100% |
| Screen | Screen blend | 100% |
| Overlay | Overlay blend | 100% |

## Build Instructions

1. Create Lerp node in Unity Shader Graph
2. Connect A and B inputs
3. Connect Factor (0-1) to T input
4. Connect output to destination

## Visual Graph Layout

```
// Basic Lerp/Mix
[A] ──> [Lerp] <─ [Factor: 0.5] ──> [Output]
        ^
        │
[B] ────┘

// Multiple blend modes
[A] ──> [Add] ──> [Output]        // Add mode
[B] ──┘

[A] ──> [Multiply] ──> [Output]   // Multiply mode
        ^
        │
[B] ────┘
```

## Pseudocode for Conversion Logic

```python
def convert_mix_node(blender_node):
    """
    Converts Blender ShaderNodeMix to Unity ShaderGraph nodes.
    1-1 direct mapping - blend mode determines the Unity node type.
    """
    # 1. Get blend mode
    blend_mode = blender_node.data_type  # 'FLOAT', 'VECTOR', 'RGBA', etc.
    mode = blender_node.blend_type  # 'MIX', 'ADD', 'SUBTRACT', 'MULTIPLY', 'SCREEN', 'OVERLAY'
    
    # 2. Get inputs
    input_a = get_input_connection(blender_node.inputs[0])  # A
    input_b = get_input_connection(blender_node.inputs[1])  # B
    factor_input = get_input_connection(blender_node.inputs["Factor"])
    
    # Get default values if not connected
    a_default = blender_node.inputs[0].default_value
    b_default = blender_node.inputs[1].default_value
    factor_default = factor_input or blender_node.inputs["Factor"].default_value
    
    # 3. Create appropriate Unity node based on blend mode
    if mode == "MIX":
        # Linear interpolation: lerp(A, B, Factor)
        unity_node = create_shadergraph_node("Lerp")
        
        if input_a:
            connect_nodes(input_a, unity_node, "A")
        else:
            unity_node.set_input("A", a_default)
        
        if input_b:
            connect_nodes(input_b, unity_node, "B")
        else:
            unity_node.set_input("B", b_default)
        
        if factor_input:
            connect_nodes(factor_input, unity_node, "T")
        else:
            unity_node.set_input("T", factor_default)
    
    elif mode == "ADD":
        # A + B (optionally scaled by factor)
        if factor_input and factor_default != 1.0:
            # A * (1-Factor) + B * Factor
            multiply_a = create_shadergraph_node("Multiply")
            if input_a:
                connect_nodes(input_a, multiply_a, "A")
            else:
                multiply_a.set_input("A", a_default)
            
            one_minus = create_shadergraph_node("One Minus")
            if factor_input:
                connect_nodes(factor_input, one_minus, "In")
            else:
                one_minus.set_input("In", factor_default)
            
            connect_nodes(one_minus, multiply_a, "B")
            
            multiply_b = create_shadergraph_node("Multiply")
            if input_b:
                connect_nodes(input_b, multiply_b, "A")
            else:
                multiply_b.set_input("A", b_default)
            
            if factor_input:
                connect_nodes(factor_input, multiply_b, "B")
            else:
                multiply_b.set_input("B", factor_default)
            
            add_node = create_shadergraph_node("Add")
            connect_nodes(multiply_a, add_node, "A")
            connect_nodes(multiply_b, add_node, "B")
            unity_node = add_node
        else:
            # Simple addition
            unity_node = create_shadergraph_node("Add")
            _connect_or_set(unity_node, "A", input_a, a_default)
            _connect_or_set(unity_node, "B", input_b, b_default)
    
    elif mode == "SUBTRACT":
        # A - B (or with factor)
        unity_node = create_shadergraph_node("Subtract")
        _connect_or_set(unity_node, "A", input_a, a_default)
        _connect_or_set(unity_node, "B", input_b, b_default)
    
    elif mode == "MULTIPLY":
        # A * B
        unity_node = create_shadergraph_node("Multiply")
        _connect_or_set(unity_node, "A", input_a, a_default)
        _connect_or_set(unity_node, "B", input_b, b_default)
    
    elif mode == "SCREEN":
        # 1 - (1-A) * (1-B) - requires Custom Function or multiple nodes
        unity_node = _create_screen_blend(input_a, a_default, input_b, b_default)
    
    elif mode == "OVERLAY":
        # Complex blend - requires Custom Function
        unity_node = _create_overlay_blend(input_a, a_default, input_b, b_default)
    
    else:
        # Default to Lerp
        unity_node = create_shadergraph_node("Lerp")
        _connect_or_set(unity_node, "A", input_a, a_default)
        _connect_or_set(unity_node, "B", input_b, b_default)
        _connect_or_set(unity_node, "T", factor_input, factor_default)
    
    return unity_node


def _connect_or_set(node, port, input_node, default_value):
    """Helper to connect input or set default value"""
    if input_node:
        connect_nodes(input_node, node, port)
    else:
        node.set_input(port, default_value)


def _create_screen_blend(a_input, a_default, b_input, b_default):
    """Create screen blend: 1 - (1-A) * (1-B)"""
    screen_func = create_shadergraph_node("Custom Function", {
        "name": "screen",
        "body": "return 1.0 - (1.0 - A) * (1.0 - B);"
    })
    _connect_or_set(screen_func, "A", a_input, a_default)
    _connect_or_set(screen_func, "B", b_input, b_default)
    return screen_func


def _create_overlay_blend(a_input, a_default, b_input, b_default):
    """Create overlay blend: A < 0.5 ? 2*A*B : 1-2*(1-A)*(1-B)"""
    overlay_func = create_shadergraph_node("Custom Function", {
        "name": "overlay",
        "body": "return A < 0.5 ? 2*A*B : 1.0 - 2.0*(1.0-A)*(1.0-B);"
    })
    _connect_or_set(overlay_func, "A", a_input, a_default)
    _connect_or_set(overlay_func, "B", b_input, b_default)
    return overlay_func
```

## Notes
- Direct 1:1 mapping to Unity Lerp
- Also supports Add, Subtract, Multiply blend modes
- Screen and Overlay require Custom Function nodes
