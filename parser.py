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

        # Node-specific properties - extract all relevant settings
        if node_type == 'ShaderNodeMath':
            node_data['properties']['operation'] = node.operation
            node_data['properties']['use_clamp'] = node.use_clamp
        elif node_type == 'ShaderNodeVectorMath':
            node_data['properties']['operation'] = node.operation
        elif node_type == 'ShaderNodeMixRGB':
            node_data['properties']['blend_mode'] = node.blend_type
            node_data['properties']['use_clamp'] = node.use_clamp
        elif node_type == 'ShaderNodeTexImage':
            if node.image:
                node_data['properties']['image_name'] = node.image.name
                node_data['properties']['image_path'] = node.image.filepath
                node_data['properties']['projection'] = node.projection
                node_data['properties']['extension'] = node.extension
                # Store image colorspace for reference
                if hasattr(node.image, 'colorspace_settings'):
                    node_data['properties']['colorspace'] = node.image.colorspace_settings.name
        elif node_type == 'ShaderNodeMapping':
            # Store mapping values
            node_data['properties']['location'] = list(node.inputs['Location'].default_value)
            node_data['properties']['rotation'] = list(node.inputs['Rotation'].default_value)
            node_data['properties']['scale'] = list(node.inputs['Scale'].default_value)
        elif node_type == 'ShaderNodeTexCoord':
            node_data['properties']['from_dupli'] = node.from_dupli
        elif node_type == 'ShaderNodeUVMap':
            node_data['properties']['uv_map'] = node.uv_map
            node_data['properties']['from_instancer'] = node.from_instancer
        elif node_type == 'ShaderNodeBsdfPrincipled':
            # Store all BSDF inputs as properties for decomposition
            for input_name in ['Base Color', 'Metallic', 'Roughness', 'Normal', 
                              'Emission', 'Emission Strength', 'IOR', 'Transmission',
                              'Transmission Roughness', 'Alpha', 'Subsurface',
                              'Subsurface Radius', 'Subsurface Color']:
                if input_name in node.inputs:
                    sock = node.inputs[input_name]
                    node_data['properties'][input_name] = self._get_socket_value(sock)
        elif node_type == 'ShaderNodeMix':
            node_data['properties']['data_type'] = node.data_type
            node_data['properties']['blend_type'] = node.blend_type
            node_data['properties']['clamp_result'] = node.clamp_result
            node_data['properties']['clamp_factor'] = node.clamp_factor
        elif node_type == 'ShaderNodeSeparateColor':
            node_data['properties']['mode'] = node.mode
        elif node_type == 'ShaderNodeCombineColor':
            node_data['properties']['mode'] = node.mode
        elif node_type == 'ShaderNodeClamp':
            node_data['properties']['clamp_type'] = node.clamp_type
            node_data['properties']['use_clamp'] = node.use_clamp
        elif node_type == 'ShaderNodeMapRange':
            node_data['properties']['data_type'] = node.data_type
            node_data['properties']['clamp'] = node.clamp
            node_data['properties']['interpolation_type'] = node.interpolation_type
        elif node_type == 'ShaderNodeValToRGB':
            node_data['properties']['color_ramp'] = node.color_ramp.name if node.color_ramp else None
            node_data['properties']['clamp'] = node.clamp
        elif node_type == 'ShaderNodeRGBToBW':
            pass  # No special properties
        elif node_type == 'ShaderNodeHueSaturation':
            node_data['properties']['hue'] = node.inputs['Hue'].default_value
            node_data['properties']['saturation'] = node.inputs['Saturation'].default_value
            node_data['properties']['value'] = node.inputs['Value'].default_value
            node_data['properties']['factor'] = node.inputs['Fac'].default_value
        elif node_type == 'ShaderNodeInvert':
            node_data['properties']['clamp_result'] = node.inputs['Fac'].default_value
        elif node_type == 'ShaderNodeBrightContrast':
            node_data['properties']['use_clamp'] = node.use_clamp

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
        except (AttributeError, TypeError) as e:
            pass
        return None
