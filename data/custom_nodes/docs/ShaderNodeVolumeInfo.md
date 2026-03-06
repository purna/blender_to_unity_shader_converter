# Blender to Unity: ShaderNodeVolumeInfo Conversion Guide

## Conversion Type: 4 (No Conversion - Not Supported)

## Overview
- **Blender Node**: `ShaderNodeVolumeInfo`
- **Unity ShaderGraph Equivalent**: Not supported
- **Category**: Input
- **Compatibility**: 25% (Minimal)

This document explains why Blender's `ShaderNodeVolumeInfo` cannot be converted to Unity ShaderGraph.

## 1. Conceptual Overview
The `ShaderNodeVolumeInfo` in Blender provides information about the volume being rendered, such as density. This is a Blender-specific node with no equivalent in Unity.

## 2. Unity Equivalent
- **None**: Volume data is not available in ShaderGraph

## 3. Parameters

| Blender Output | Type | Unity Implementation | Notes |
|---------------|------|---------------------|-------|
| Density | Float | Not available | Must be manually set |

## 4. Limitations
- Volume information is not exposed in Unity shaders
- No equivalent node in ShaderGraph
- Must manually create volume properties

## 5. Pseudocode for Conversion Logic

```python
def convert_volume_info_node(blender_node):
    log_error(
        "Volume Info node is not supported in Unity ShaderGraph. "
        "Volume properties must be set manually in the shader."
    )
    return None
```

## 6. Summary
- **Not Compatible**: Volume data cannot be accessed in Unity shaders
- Manual setup required for volume properties
- This is a Blender-specific feature with no direct equivalent
