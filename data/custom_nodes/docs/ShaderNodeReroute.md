# ShaderNodeReroute

## Conversion Type: 1-1 (Direct Mapping)

## Overview
- **Blender Node**: ShaderNodeReroute
- **Category**: Utility
- **Compatibility**: 100%

## Unity Equivalent
**Node Reroute** - Direct 1:1 mapping

## Conversion Process

### Step 1: Direct Port
- **Description**: Reroute/pass-through node - organizes graph connections
- **Blender Input**: Any connection
- **Unity Output**: Same connection passed through

## Build Instructions

1. Create Node Reroute in Unity Shader Graph
2. Connect input to output
3. Use for organizing messy connections

## Visual Graph Layout

```
// Reroute simply passes through
[Any Node Output] ──> [Reroute] ──> [Any Node Input]

// Can chain multiple reroutes
[Output] ──> [Reroute 1] ──> [Reroute 2] ──> [Input]
```

## Pseudocode for Conversion Logic

```python
def convert_reroute_node(blender_node):
    """
    Converts Blender ShaderNodeReroute to Unity ShaderGraph Node Reroute.
    1-1 direct mapping - this is purely a graph organization node.
    """
    # 1. Get the input connection to this reroute
    input_connection = get_input_connection(blender_node.inputs[0])
    
    # 2. In Unity, a reroute is created at the connection point
    # rather than as a separate node. The conversion should:
    # - Skip creating an actual reroute node
    # - Simply redirect connections directly
    
    if input_connection:
        # Instead of creating a reroute node, we track this reroute
        # as a connection point that can be used by downstream nodes
        reroute_point = create_reroute_point(
            node_type="Reroute",
            connection=input_connection
        )
        return reroute_point
    
    # If no input, create a placeholder reroute (unconnected)
    return create_shadergraph_node("Reroute")


def optimize_reroutes(unity_graph):
    """
    Post-process: Unity doesn't need explicit reroute nodes.
    Connections can be made directly. This function removes
    unnecessary reroute nodes and reconnects directly.
    """
    for reroute_node in unity_graph.get_nodes(type="Reroute"):
        input_conn = reroute_node.get_input_connection(0)
        output_conns = reroute_node.get_output_connections(0)
        
        if input_conn and output_conns:
            # Direct connect: input -> each output
            for out_conn in output_conns:
                unity_graph.connect(input_conn, out_conn.target, out_conn.target_port)
            
            # Remove the reroute node
            unity_graph.remove_node(reroute_node)
```

## Notes
- Fully compatible - helper/utility node
- Used for organizing node graphs
- In practice, Unity can often skip creating reroute nodes and just connect directly
