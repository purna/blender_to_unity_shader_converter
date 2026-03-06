# ShaderNodeMixShader

## Conversion Type: 3 (Multi-Node Conversion)

## Overview
- **Blender Node**: ShaderNodeMixShader
- **Category**: Shader
- **Compatibility**: 85%

## Unity Equivalent
Multiple **Lerp** nodes to blend PBR properties between two shader branches

## Conversion Process

### Step 1: Decompose Shaders
- **Description**: Extract material properties from both shaders
- **Blender Input**: Shader1, Shader2, Factor
- **Unity Output**: Base color, Metallic, Smoothness values

### Step 2: Blend Properties
- **Description**: Lerp between property values using factor
- **Blender Input**: Property values from both shaders
- **Unity Output**: Blended property values

### Step 3: Connect to Master
- **Description**: Connect blended properties to PBR Master
- **Blender Input**: Blended values
- **Unity Output**: Final material

## Blender to Unity Mapping

| Blender Parameter | Unity Implementation | Compatibility |
|-------------------|---------------------|---------------|
| Fac | Lerp factor | 100% |
| Shader1 | Property set 1 | 85% |
| Shader2 | Property set 2 | 85% |

## Build Instructions

1. Extract properties from first shader (Color, Metallic, Smoothness, etc.)
2. Extract properties from second shader
3. Create Lerp nodes for each property
4. Connect factor to all Lerp nodes
5. Connect blended outputs to PBR Master inputs

## Visual Graph Layout

```
// Complex: Blending two PBR materials
// Branch 1: First material properties
[Color1] ──> [Metallic1] ──> [Smoothness1] ──┐
                                                 ├─> [Lerp] ──> [Base Color]
[Color2] ──> [Metallic2] ──> [Smoothness2] ──┘     ^
                                                 [Factor: 0.5]

// Full material blending
[Material A] ──> Extract Properties ─┬─> [Lerp per property] ──> [PBR Master]
                                     │                      ^
[Material B] ──> Extract Properties ─┤               [Factor]
                                     │
[Blend Factor] ──────────────────────┘
```

## Pseudocode for Conversion Logic

```python
def convert_mix_shader_node(blender_node):
    """
    Converts Blender ShaderNodeMixShader to Unity ShaderGraph nodes.
    Multi-node conversion - must decompose shaders and blend individual properties.
    """
    # 1. Get inputs
    shader1_input = get_input_connection(blender_node.inputs["Shader1"])
    shader2_input = get_input_connection(blender_node.inputs["Shader2"])
    factor_input = get_input_connection(blender_node.inputs["Fac"])
    
    factor_value = factor_input or blender_node.inputs["Fac"].default_value
    
    # 2. Extract properties from each shader branch
    # This requires recursively tracing the shader trees
    shader1_props = extract_bsdf_properties(shader1_input) if shader1_input else {}
    shader2_props = extract_bsdf_properties(shader2_input) if shader2_input else {}
    
    # 3. Create Lerp nodes for each property
    blended_props = {}
    
    # Properties to blend
    property_names = ["BaseColor", "Metallic", "Roughness", "Normal", "Emission", "Alpha"]
    
    for prop_name in property_names:
        val1 = shader1_props.get(prop_name)
        val2 = shader2_props.get(prop_name)
        
        if val1 is not None or val2 is not None:
            # Create Lerp node
            lerp_node = create_shadergraph_node("Lerp")
            
            # Connect or set default values
            if val1 is not None:
                connect_or_set(lerp_node, "A", val1)
            else:
                lerp_node.set_input("A", get_default_for_property(prop_name))
            
            if val2 is not None:
                connect_or_set(lerp_node, "B", val2)
            else:
                lerp_node.set_input("B", get_default_for_property(prop_name))
            
            # Connect factor
            if factor_input:
                connect_nodes(factor_input, lerp_node, "T")
            else:
                lerp_node.set_input("T", factor_value)
            
            blended_props[prop_name] = lerp_node
    
    # 4. Return blended properties dict
    return blended_props


def extract_bsdf_properties(shader_socket):
    """
    Recursively extract all PBR properties from a shader branch.
    Returns dict of property_name -> node
    """
    if shader_socket is None:
        return {}
    
    # Get the actual node from socket
    node = get_node_from_socket(shader_socket)
    
    props = {}
    
    if node.type == "BSDF_PRINCIPLED":
        # Principled BSDF has many properties
        props["BaseColor"] = get_input_connection(node.inputs["Base Color"])
        props["Metallic"] = get_input_connection(node.inputs["Metallic"])
        props["Roughness"] = get_input_connection(node.inputs["Roughness"])
        props["Normal"] = get_input_connection(node.inputs["Normal"])
        props["Emission"] = get_input_connection(node.inputs["Emission"])
        props["Alpha"] = get_input_connection(node.inputs["Alpha"])
        props["Subsurface"] = get_input_connection(node.inputs["Subsurface"])
        props["Specular"] = get_input_connection(node.inputs["Specular IOR Level"])
        # ... handle other Principled BSDF inputs
    
    elif node.type == "EMISSION":
        props["Emission"] = get_input_connection(node.inputs["Color"])
    
    elif node.type == "MIX_SHADER":
        # Nested mix - recursively extract
        nested_props = convert_mix_shader_node(node)
        props.update(nested_props)
    
    # Handle other shader types...
    
    return props


def get_default_for_property(prop_name):
    """Get default value for a PBR property"""
    defaults = {
        "BaseColor": (0.5, 0.5, 0.5, 1.0),
        "Metallic": 0.0,
        "Roughness": 0.5,
        "Normal": (0, 0, 1),
        "Emission": (0, 0, 0, 0),
        "Alpha": 1.0
    }
    return defaults.get(prop_name, 0.0)


def connect_or_set(node, port, value):
    """Connect a socket or set a default value"""
    if value is not None and hasattr(value, 'outputs'):
        # It's a node/socket
        connect_nodes(value, node, port)
    else:
        # It's a literal value
        node.set_input(port, value)
```

## Notes
- Blends PBR properties, not complete shaders
- Works for simple material transitions
- 15% loss - cannot blend complex features (SSS, anisotropy)
- Requires extracting properties from upstream shader nodes
- Must create separate Lerp for each property being blended
