# UV Map Node

## Overview
The UV Map node outputs UV texture coordinates from a mesh's UV layers. UV coordinates determine how 2D textures map onto 3D geometry.

## Blender Node Inputs
- **UV Layer**: Select which UV map to use (UV0, UV1, UV2, etc.)

## Blender Node Outputs
- **UV**: UV coordinates as Vector (2 channels)

## Unity Equivalent

### Primary Option: UV Node
Unity Shader Graph has a built-in UV node that provides texture coordinates.

### Secondary Option: Vertex UV
Use the "Vertex Color" or custom vertex attributes to pass UV data.

### Custom Implementation for Multiple UV Sets
For multiple UV channels, create a custom property for each UV set:

```
1. Add a Vector4 property for each UV channel
2. Connect to texture Sample nodes
3. Name properties: UV0, UV1, UV2, etc.
```

## Conversion Strategy

### Simple Case (Single UV Map)
- Use built-in UV node in Unity
- Connect directly to texture Sample nodes

### Multi-UV Case (Multiple UV Channels)
1. Create Vector4 properties in Shader Graph:
   - UV0 (XY = first UV channel)
   - UV1 (XY = second UV channel)
2. Pass UV coordinates from mesh via material properties
3. Use C# script to set UV coordinates from Blender

### C# Script for UV Extraction
```csharp
// Attach to mesh renderer to pass UV coordinates
public class UVPasser : MonoBehaviour
{
    public int uvChannel = 0;
    
    void Start()
    {
        Mesh mesh = GetComponent<MeshFilter>().mesh;
        Vector2[] uvs = mesh.uv;
        if (uvChannel > 0 && mesh.uv2 != null) 
            uvs = mesh.uv2;
        
        GetComponent<Renderer>().material.SetVector("_UV0", 
            new Vector4(uvs[0].x, uvs[0].y, 0, 0));
    }
}
```

## Compatibility
- **Compatibility**: 95%
- **Notes**: Direct mapping for primary UV. Multiple UV channels require custom properties.

## Additional Resources
- [Unity Shader Graph UV Node Documentation](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest/index.html?subfolder=/manual/UV-Node.html)
- [Blender UV Map Node Manual](https://docs.blender.org/manual/en/latest/render/shader_nodes/input/uv_map.html)
