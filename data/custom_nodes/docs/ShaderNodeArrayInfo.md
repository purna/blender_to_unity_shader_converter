# Blender to Unity: ShaderNodeArrayInfo Conversion Guide

## Conversion Type: 4 (No Conversion - Not Possible)

## Overview
- **Blender Node**: `ShaderNodeArrayInfo`
- **Unity ShaderGraph Equivalent**: None
- **Category**: Input / Geometry
- **Compatibility**: 0% (Incompatible)

This document explains why Blender's `ShaderNodeArrayInfo` node cannot be converted to Unity ShaderGraph and outlines alternative approaches in Unity.

## 1. Conceptual Incompatibility
- **Blender**: The `ShaderNodeArrayInfo` node is a special node that works directly with the **Array Modifier**. It allows a material to know which copy of the mesh it is rendering (e.g., "instance 3 of 10"). This is a unique integration between Blender's modifier stack and its shader system.
- **Unity**: Unity's shader system is decoupled from the modeling-time constructs of another application. A mesh in Unity is just a collection of vertices; the shader has no inherent knowledge of whether that mesh was once part of a Blender `Array` modifier.

**There is no equivalent node or system in ShaderGraph.** The data this node provides simply does not exist at shader execution time in Unity.

## 2. Conversion and Recreation Strategy
Automated conversion is impossible. The effect must be manually recreated in Unity using entirely different techniques.

### Step 1: Analyze the Blender Setup
Determine *why* the `ShaderNodeArrayInfo` node is being used. Is it to change the color of each copy? To alter its position? To animate it based on its index?

### Step 2: Choose a Unity Technique

#### Alternative A: Manual Duplication (Simple Cases)
- **Description**: If the array is not dynamic, the simplest solution is to apply the Array Modifier in Blender before exporting.
- **Workflow**:
    1. In Blender, apply the `Array` modifier. This creates real, distinct geometry for each copy.
    2. You can then assign different materials or vertex colors to each copy manually.
    3. Export the combined mesh to Unity.
- **Limitation**: This creates much larger mesh files and is not suitable for a large number of copies or dynamic effects.

#### Alternative B: Script-Based GPU Instancing (Advanced Cases)
- **Description**: This is the "correct" but much more advanced way to handle instancing in Unity. It involves writing a C# script to pass per-instance data to the shader.
- **Workflow**:
    1. In your Unity shader, create properties to receive the instance data (e.g., a `Float` property called `_InstanceIndex`).
    2. Write a C# script that uses `Graphics.DrawMeshInstanced` or a similar method.
    3. In the script, create a `MaterialPropertyBlock` for each instance and set the `_InstanceIndex` value.
    4. Apply this property block when drawing the instances.
- **Limitation**: This requires C# programming and a deep understanding of Unity's rendering pipeline. It cannot be achieved with ShaderGraph alone.

## 3. Pseudocode for Conversion Logic
The converter's only job is to identify the incompatible node and warn the user.

```python
def convert_array_info_node(blender_node):
  # 1. Detect that an Array Info node is being used.
  is_array_info_node_present = True

  # 2. Log a critical error message explaining the incompatibility.
  log_error(
    "The material uses a 'ShaderNodeArrayInfo' node. This node is " \
    "tied to Blender's Array Modifier and has no equivalent in Unity ShaderGraph. " \
    "The effect must be recreated manually in Unity, either by applying " \
    "the modifier in Blender before export or by using an advanced, script-based " \
    "GPU instancing workflow with MaterialPropertyBlocks."
  )

  # 3. Return nothing, as no nodes can be created.
  return None
```

## 4. Summary
Direct conversion of `ShaderNodeArrayInfo` is not possible. The user must manually decide on a new implementation strategy within Unity based on their specific needs, as the original method is fundamentally tied to Blender's architecture.
