# ShaderNodeFresnel

## Conversion Type: 1-1 (Direct Mapping)

## Overview
- **Source**: Blender Cycles/Eevee
- **Target**: Unity URP/HDRP
- **Category**: Input
- **Compatibility**: 95%

## Unity Equivalent
- **Primary**: Fresnel Effect node
- **Implementation**: Direct mapping

## Conversion Process

### Step 1: Create Fresnel Node
- Add Fresnel Effect node in Unity

### Step 2: Connect Normal
- Connect Normal input if available

## Parameters

| Blender | Type | Unity | Notes |
|---------|------|-------|-------|
| Normal | Vector3 | Normal | Optional |
| IOR | Float | Power | Direct |

## Visual Graph Layout

```
// Simple Fresnel setup
[Vector3: Normal] ──> [Fresnel Effect] ──> [Output]
                              ^
                              │
[Float: IOR=1.45] ────────────┘

// Fresnel used for rim lighting
[Fresnel Effect] ──> [Multiply] ──> [PBR Master].[Emission]
                                        ^
                                        │
[Color: Gold] ──────────────────────────┘
```

## Pseudocode for Conversion Logic

```python
def convert_fresnel_node(blender_node):
    """
    Converts Blender ShaderNodeFresnel to Unity ShaderGraph Fresnel Effect node.
    1-1 direct mapping with slight parameter name difference.
    """
    # 1. Create Unity Fresnel Effect node
    unity_fresnel = create_shadergraph_node("Fresnel Effect")
    
    # 2. Map IOR to Power parameter
    # Blender uses IOR (Index of Refraction), Unity uses Power
    # Formula: Power = (1 - IOR)^2 or can use IOR directly in custom function
    blender_ior = blender_node.inputs["IOR"].default_value
    
    # Standard Fresnel power approximation from IOR
    # For typical IOR values (1.0 - 2.5), power ranges roughly 0-5
    power_value = (blender_ior - 1.0) ** 2
    unity_fresnel.set_property("Power", power_value)
    
    # 3. Connect Normal input if available
    normal_input = get_input_connection(blender_node.inputs["Normal"])
    if normal_input:
        connect_nodes(normal_input, unity_fresnel, "Normal")
    
    # 4. Set Fresnel type if needed (None, Pelican, Schlick)
    # Blender Fresnel is Schlick-approximated
    unity_fresnel.set_property("Fresnel Type", "Schlick")
    
    return unity_fresnel
```

## Compatibility Notes
- 95% compatible - direct mapping
- Uses Fresnel equation based on view angle
- IOR to Power conversion is approximate

## Limitations
- None significant
