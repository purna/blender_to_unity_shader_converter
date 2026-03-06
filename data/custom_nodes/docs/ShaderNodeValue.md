# Blender to Unity: ShaderNodeValue Conversion Guide

## Overview
- **Blender Node**: `ShaderNodeValue`
- **Unity ShaderGraph Node**: `Float` Node or `Float` Property
- **Category**: Input
- **Compatibility**: 100%

This document provides a guide for converting Blender's `ShaderNodeValue` into a numeric constant in Unity's ShaderGraph.

## 1. Unity ShaderGraph Node Identification
The `ShaderNodeValue` from Blender, which provides a single floating-point number, has two common equivalents in Unity ShaderGraph:

1.  **Float Node**: A hardcoded, constant value inside the graph. It cannot be changed from the Material Inspector.
2.  **Float Property**: A parameter exposed in the Material Inspector. This is the more flexible and common choice.

The best practice is to convert a `ShaderNodeValue` to a **Float Property** on the ShaderGraph Blackboard.

## 2. Step-by-Step Creation in ShaderGraph

### Method 1: Creating an Exposed Float Property (Recommended)
1.  In the top-left of the ShaderGraph editor, open the **Blackboard**.
2.  Click the **+** icon and select **Float**.
3.  A new property will appear. Rename it to something descriptive (e.g., "RoughnessAmount").
4.  In the **Graph Inspector** (with the new property selected), set its **Default** value to match the value from the Blender `ShaderNodeValue`.
5.  **Drag** the property from the Blackboard onto the graph to create a `Float` property node.

### Method 2: Creating a Hardcoded Float Node
1.  Right-click on the graph and select **Create Node → Input → Basic → Float**.
2.  A `Float` node will appear. You can enter a number directly into the node's text field.

## 3. Parameter Configuration

| Blender Node | Unity Equivalent | Configuration |
|---|---|---|
| `ShaderNodeValue` | `Float` Property | Set the **Default** value in the Graph Inspector. |
| `ShaderNodeValue` | `Float` Node | Type the value directly into the node on the graph. |

## 4. Visual Graph Layout
A `Float` node is a basic input, providing a single value to other nodes.

**Expected Layout (Using a Property):**
```
[Float Property Node (e.g., "Metallic")] --(Out)--> [PBR Master Node].[Metallic]
```

## 5. Pseudocode for Conversion Logic
The conversion logic should prioritize creating exposed properties for better material customization.

```python
def convert_value_node(blender_node):
  # 1. Get the value from the Blender node
  node_value = blender_node.outputs["Value"].default_value
  
  # 2. Get a descriptive name for the property.
  # This might come from the node's label in Blender or be inferred.
  property_name = blender_node.label or "MyFloatValue"

  # 3. Create a new Float property on the ShaderGraph Blackboard
  unity_property = create_shadergraph_property("Float", property_name)
  
  # 4. Set the default value for the property
  unity_property.set_default_value(node_value)

  # 5. Create the property node on the graph
  unity_node = create_property_node_on_graph(unity_property)

  # 6. Return the new node for connection
  return unity_node
```

## 6. Limitations and Compatibility Notes
- **No Limitations**: This is a direct 1:1 functional mapping. The concept of a single float value is fundamental to both Blender and Unity shading systems.
- **Best Practices**: While you can use a hardcoded `Float` node for internal calculations, any `ShaderNodeValue` that a user is likely to want to tweak (like a multiplier for roughness, metallic, etc.) should always be converted to an exposed `Float` property on the Blackboard.
