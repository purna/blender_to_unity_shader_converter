# JSON Schema Upgrade Instructions

This document outlines the process for upgrading the JSON conversion files to support automated Unity ShaderGraph generation.

## Overview

The current JSON files contain basic metadata but lack the detailed information needed to programmatically create Unity ShaderGraphs. This guide explains how to upgrade each JSON file to include all necessary data for automated conversion.

## Why This Matters

For the plugin to automatically generate Unity ShaderGraphs, each JSON must contain:
1. **Exact Unity node types** - Not just "Add" but the full ShaderGraph node class
2. **Socket/Port definitions** - Input and output ports with types
3. **Connection logic** - How nodes connect to each other
4. **Default values** - What values to use when inputs aren't connected

---

## JSON Schema Structure

Each upgraded JSON file should follow this structure:

```json
{
  "metadata": {
    "source_node": "ShaderNodeMixShader",
    "source_engine": "Blender Cycles",
    "target_engine": "Unity",
    "target_version": "URP/HDRP",
    "conversion_rate": "100%",
    "description": "Mix shaders - direct mapping to Unity",
    "category": "Shader"
  },
  
  "unity_node": {
    "node_type": "UnityEditor.ShaderGraph.AddNode",
    "display_name": "Add",
    "category": "Math/Operator"
  },
  
  "inputs": [
    {
      "name": "Shader1",
      "socket_name": "A",
      "type": "AbstractShaderProperty",
      "required": false,
      "default_value": null
    }
  ],
  
  "outputs": [
    {
      "name": "Shader",
      "socket_name": "Out",
      "type": "AbstractShaderPort"
    }
  ],
  
  "connections": [],
  
  "blender_to_unity_mapping": [
    {
      "blender_parameter": "Shader1",
      "unity_socket": "A",
      "conversion": "direct"
    }
  ],
  
  "build_instructions": []
}
```

---

## Detailed Field Definitions

### 1. metadata
Contains basic information about the conversion.

| Field | Type | Description |
|-------|------|-------------|
| source_node | string | Blender node type name |
| source_engine | string | "Blender Cycles" or "Blender Eevee" |
| target_engine | string | "Unity" |
| target_version | string | "URP", "HDRP", or "URP/HDRP" |
| conversion_rate | string | Percentage or "100%" |
| description | string | Brief description |
| category | string | Node category |

### 2. unity_node
**NEW** - Contains Unity-specific node information.

| Field | Type | Description |
|-------|------|-------------|
| node_type | string | Full Unity class path (e.g., "UnityEditor.ShaderGraph.AddNode") |
| display_name | string | Display name in ShaderGraph |
| category | string | Menu category path |

### 3. inputs
**NEW** - Array of input socket definitions.

| Field | Type | Description |
|-------|------|-------------|
| name | string | Blender input name (for reference) |
| socket_name | string | **CRITICAL** - Exact Unity socket name |
| type | string | Data type (see Type Reference below) |
| required | boolean | Whether input must be connected |
| default_value | any | Default value if not connected |

### 4. outputs
**NEW** - Array of output socket definitions.

| Field | Type | Description |
|-------|------|-------------|
| name | string | Blender output name (for reference) |
| socket_name | string | **CRITICAL** - Exact Unity socket name |
| type | string | Data type |

### 5. connections
**NEW** - Internal node chain connections.

```json
"connections": [
  {
    "from_socket": "Out",
    "to_socket": "A",
    "node_id": "multiplication_node"
  }
]
```

### 6. blender_to_unity_mapping
Maps Blender parameters to Unity sockets.

| Field | Type | Description |
|-------|------|-------------|
| blender_parameter | string | Parameter name in Blender |
| unity_socket | string | Target Unity socket name |
| conversion | string | "direct", "inverse", or formula |

---

## Unity Socket Type Reference

Use these standard type names:

| Type | Description |
|------|-------------|
| Vector1 | Single float |
| Vector2 | Two floats (UV, offset) |
| Vector3 | Three floats (position, color RGB) |
| Vector4 | Four floats (color RGBA) |
| DynamicVector1 | Flexible single value |
| DynamicVector4 | Flexible multi-component |
| AbstractShaderProperty | Shader input |
| AbstractShaderPort | Shader output |
| Texture2D | Texture reference |
| SamplerState | Sampler settings |
| Normal | Normal vector |
| Shader | Shader (shader-to-shader) |

---

## Common Unity Node Types

| Blender Node | Unity Node Type | Category |
|-------------|-----------------|----------|
| Mix Shader | AddNode | Math/Operator |
| Add Shader | AddNode | Math/Operator |
| Math | AddNode/SubtractNode/etc | Math/Operator |
| Separate XYZ | SplitNode | Channel |
| Combine XYZ | CombineNode | Channel |
| Sample Texture | SampleTexture2DNode | Texture |
| UV | UVNode | Geometry |
| Position | PositionNode | Geometry |
| Normal | NormalNode | Geometry |
| Fresnel | FresnelEffectNode | Math |
| Lerp | LerpNode | Math |

---

## Step-by-Step Upgrade Process

### Step 1: Identify the Unity Node
1. Determine which Unity ShaderGraph node performs the same function
2. Find the exact node class name (see Common Unity Node Types)
3. Note the menu category

### Step 2: Define Input Sockets
For each Blender input:
1. Find the corresponding Unity socket
2. Determine the socket name (case-sensitive!)
3. Note the data type
4. Set default value from Blender

### Step 3: Define Output Sockets
For each Blender output:
1. Identify the Unity output socket
2. Note the exact socket name
3. Specify the output type

### Step 4: Add Internal Connections
If the conversion requires a node chain:
1. Define additional nodes in the chain
2. Specify connections between nodes

### Step 5: Verify Mapping
Ensure every Blender parameter has a Unity socket mapping.

---

## Example: Upgrading ShaderNodeMixShader

### Before (Insufficient):
```json
{
  "metadata": { "source_node": "ShaderNodeMixShader" },
  "unity_equivalent": "Add",
  "blender_parameters": [
    { "name": "Shader1", "type": "Shader" },
    { "name": "Shader2", "type": "Shader" },
    { "name": "Fac", "type": "Float" }
  ]
}
```

### After (Complete):
```json
{
  "metadata": {
    "source_node": "ShaderNodeMixShader",
    "source_engine": "Blender Cycles",
    "target_engine": "Unity",
    "target_version": "URP/HDRP",
    "conversion_rate": "100%",
    "description": "Mix shaders - direct mapping to Unity",
    "category": "Shader"
  },
  
  "unity_node": {
    "node_type": "UnityEditor.ShaderGraph.AddNode",
    "display_name": "Add",
    "category": "Math/Operator"
  },
  
  "inputs": [
    {
      "name": "Shader1",
      "socket_name": "A",
      "type": "AbstractShaderProperty",
      "required": false,
      "default_value": null
    },
    {
      "name": "Shader2", 
      "socket_name": "B",
      "type": "AbstractShaderProperty",
      "required": false,
      "default_value": null
    },
    {
      "name": "Fac",
      "socket_name": "C",
      "type": "Vector1",
      "required": false,
      "default_value": 0.5
    }
  ],
  
  "outputs": [
    {
      "name": "Shader",
      "socket_name": "Out",
      "type": "AbstractShaderPort"
    }
  ],
  
  "connections": [],
  
  "blender_to_unity_mapping": [
    {
      "blender_parameter": "Shader1",
      "unity_socket": "A",
      "conversion": "direct"
    },
    {
      "blender_parameter": "Shader2",
      "unity_socket": "B", 
      "conversion": "direct"
    },
    {
      "blender_parameter": "Fac",
      "unity_socket": "C",
      "conversion": "direct"
    }
  ]
}
```

---

## Testing Your Upgraded JSON

After upgrading a JSON file:

1. **Validate JSON syntax** - Use a JSON validator
2. **Check socket names** - Must match Unity API exactly
3. **Verify mappings** - Every Blender parameter should map to a Unity socket
4. **Test with plugin** - Run the conversion and check the output

---

## Priority Order

Upgrade JSON files in this order:

1. **High Priority** (most commonly used):
   - ShaderNodeMath
   - ShaderNodeMixShader
   - ShaderNodeAddShader
   - ShaderNodeMixRGB
   - ShaderNodeTexImage

2. **Medium Priority**:
   - ShaderNodeBsdfPrincipled
   - ShaderNodeSeparateXYZ
   - ShaderNodeCombineXYZ
   - ShaderNodeMapping

3. **Lower Priority**:
   - Texture nodes
   - Complex shader nodes

---

## Notes

- Socket names are **case-sensitive** in Unity ShaderGraph
- Use `UnityEditor.ShaderGraph.*Node` class names
- Test each conversion after upgrading
- Keep the documentation consistent across all files
