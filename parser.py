"""
Blender Shader Parser
Extracts node graph data from Blender materials
"""

import bpy
from typing import Dict, List, Any

class BlenderShaderParser:
    """Parse Blender shader graphs and extract node information"""
    
    def __init__(self, material: bpy.types.Material):
        self.material = material
        self.node_tree = material.node_tree
        self.nodes_data = {}
        self.connections = []

    def parse(self) -> Dict:
        """Extract shader graph structure"""
        result = {
            'name': self.material.name,
            'nodes': [],
            'connections': [],
            'textures': []
        }

        # Parse all nodes
        for node in self.node_tree.nodes:
            node_data = self._parse_node(node)
            if node_data:
                result['nodes'].append(node_data)
                self.nodes_data[node.name] = node_data

        # Parse connections
        for link in self.node_tree.links:
            conn = self._parse_connection(link)
            if conn:
                result['connections'].append(conn)

        return result

    def _parse_node(self, node: bpy.types.Node) -> Dict:
        """Parse individual node"""
        node_type = node.bl_idname
        
        node_data = {
            'name': node.name,
            'blender_type': node_type,
            'inputs': {},
            'outputs': {},
            'properties': {}
        }

        # Extract inputs
        for input_socket in node.inputs:
            if input_socket.enabled:
                node_data['inputs'][input_socket.name] = {
                    'type': str(input_socket.type),
                    'default': self._get_socket_value(input_socket)
                }

        # Extract outputs
        for output_socket in node.outputs:
            if output_socket.enabled:
                node_data['outputs'][output_socket.name] = {
                    'type': str(output_socket.type)
                }

        # Node-specific properties
        if node_type == 'ShaderNodeMath':
            node_data['properties']['operation'] = node.operation
        elif node_type == 'ShaderNodeMixRGB':
            node_data['properties']['use_clamp'] = node.use_clamp
        elif node_type == 'ShaderNodeTexImage':
            if node.image:
                node_data['properties']['image_name'] = node.image.name
                node_data['properties']['image_path'] = node.image.filepath
        elif node_type == 'ShaderNodeMapping':
            # Store mapping values
            node_data['properties']['location'] = list(node.inputs['Location'].default_value)
            node_data['properties']['rotation'] = list(node.inputs['Rotation'].default_value)
            node_data['properties']['scale'] = list(node.inputs['Scale'].default_value)

        return node_data

    def _parse_connection(self, link: bpy.types.NodeLink) -> Dict:
        """Parse node connections"""
        return {
            'from_node': link.from_node.name,
            'from_socket': link.from_socket.name,
            'to_node': link.to_node.name,
            'to_socket': link.to_socket.name,
            'from_type': str(link.from_socket.type),
            'to_type': str(link.to_socket.type)
        }

    @staticmethod
    def _get_socket_value(socket: bpy.types.NodeSocket) -> Any:
        """Get socket default value"""
        try:
            if hasattr(socket, 'default_value'):
                val = socket.default_value
                if isinstance(val, (int, float)):
                    return float(val)
                elif hasattr(val, '__iter__'):
                    return list(val)
                return val
        except:
            pass
        return None
