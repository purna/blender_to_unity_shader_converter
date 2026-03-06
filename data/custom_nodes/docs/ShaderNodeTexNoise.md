# ShaderNodeTexNoise

## Conversion Type: 2 (Near Conversion)

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Texture
- **Compatibility**: 80%

## Unity Equivalent
- **Primary**: Simple Noise Node
- **Implementation**: Near mapping with parameter differences

## Blender Node Description
Noise Texture - procedural Perlin or Voronoi noise with adjustable scale, detail, and roughness.

## Conversion Process

### Step 1: Create Simple Noise
- Add Simple Noise node in Unity
- Connect UV

### Step 2: Configure Scale
- Set Scale for noise frequency

### Step 3: Add Detail
- Add multiple octaves using fractal
- Use for more detail

## Parameters

| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Vector | Vector | UV | Direct |
| Scale | Float | Scale | Direct |
| Detail | Float | Octaves | Partial |
| Roughness | Float | Lacunarity | Partial |

## Visual Graph Layout

```
// Basic Noise setup
[UV] ──> [Simple Noise] ──> [Output]

// With Scale
[UV] ──> [Simple Noise] ──> [Multiply] ──> [Output]
              ^                   ^
              │                   │
[Float: 5.0] ─┴───────────────────┘

// Fractal Noise (detail)
[UV] ──> [Simple Noise] ──┬─> [Add] ──> [Output]
                          │
[UV] ──> [Simple Noise] ──┘
        (higher scale)
```

## Pseudocode for Conversion Logic

```python
def convert_texnoise_node(blender_node):
    """
    Converts Blender ShaderNodeTexNoise to Unity ShaderGraph Simple Noise node.
    Near conversion - different noise algorithms but similar output.
    """
    # 1. Create Unity Simple Noise node
    unity_noise = create_shadergraph_node("Simple Noise")
    
    # 2. Get input connections
    vector_input = get_input_connection(blender_node.inputs["Vector"])
    scale_input = get_input_connection(blender_node.inputs["Scale"])
    detail_input = get_input_connection(blender_node.inputs["Detail"])
    roughness_input = get_input_connection(blender_node.inputs["Roughness"])
    
    # 3. Set default scale
    default_scale = blender_node.inputs["Scale"].default_value
    unity_noise.set_property("Scale", default_scale)
    
    # 4. Connect UV/Vector
    if vector_input:
        connect_nodes(vector_input, unity_noise, "UV")
    else:
        # Use default UV from Coordinate node
        default_uv = create_shadergraph_node("UV")
        connect_nodes(default_uv, unity_noise, "UV")
    
    # 5. Handle Detail (octaves) - Blender uses Detail differently than Unity
    # Blender Detail adds more noise layers (octaves)
    # Unity's Simple Noise doesn't have direct octave support
    detail_value = blender_node.inputs["Detail"].default_value
    
    if detail_value > 0:
        # Create fractal noise by adding multiple noise layers
        detail_noise = create_shadergraph_node("Simple Noise")
        
        # Scale up for detail layer
        scale_mult = create_shadergraph_node("Multiply")
        scale_mult.set_input("A", default_scale * 2.0)  # Higher frequency
        scale_mult.set_input("B", detail_value / 10.0)  # Scaled detail
        
        connect_nodes(vector_input or default_uv, detail_noise, "UV")
        
        # Add to main noise
        add_node = create_shadergraph_node("Add")
        connect_nodes(unity_noise, add_node, "A")
        connect_nodes(detail_noise, add_node, "B")
        
        unity_noise = add_node
    
    # 6. Handle Roughness (lacunarity)
    # Blender roughness affects the noise pattern smoothness
    # Unity doesn't have direct equivalent - would need custom function
    roughness_value = blender_node.inputs["Roughness"].default_value
    
    if roughness_value != 2.0:  # Default in Blender
        # Add warning about lacunarity not being fully supported
        log_warning(
            f"TexNoise: Roughness value {roughness_value} cannot be "
            "fully converted. Unity Simple Noise uses fixed algorithm."
        )
    
    return unity_noise
```

## Compatibility Notes
- 80% compatible - basic noise works
- Different noise algorithm (Unity uses different Perlin implementation)
- Detail and Roughness are approximations only

## Limitations
- Different noise implementation
- Less control than Blender
- Voronoi noise type not directly supported in Unity
