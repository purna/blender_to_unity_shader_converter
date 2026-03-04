"""
Shader Graph Converter
Main conversion engine with strategy routing
"""

import uuid
from typing import Dict
from . import socket_handler, strategies, utils

class UnityShaderGraphNode:
    """Represents a Unity Shader Graph node"""
    def __init__(self, node_type: str, guid: str = None):
        self.guid = guid or str(uuid.uuid4())
        self.node_type = node_type
        self.properties = {}
        self.inputs = {}
        self.outputs = {}
        self.conversion_chain = None  # Store conversion steps from JSON

    def to_dict(self) -> Dict:
        return {
            'm_ObjectId': self.guid,
            'm_Group': 0,
            'm_Name': self.node_type,
            'm_SerializableSlots': [],
            'conversion_chain': self.conversion_chain
        }


class UnityShaderGraph:
    """Manages a complete Unity Shader Graph"""
    def __init__(self, name: str = "ConvertedShader"):
        self.name = name
        self.guid = str(uuid.uuid4())
        self.nodes = {}
        self.edges = []
        self.properties = []
        self.conversion_chains = {}  # Store all conversion chains for export

    def add_node(self, node_type: str, guid: str = None) -> UnityShaderGraphNode:
        node = UnityShaderGraphNode(node_type, guid)
        self.nodes[node.guid] = node
        return node

    def add_edge(self, output_guid: str, output_slot: int, input_guid: str, input_slot: int):
        """Connect two nodes"""
        self.edges.append({
            'outputNode': output_guid,
            'outputSlot': output_slot,
            'inputNode': input_guid,
            'inputSlot': input_slot
        })

    def add_conversion_chain(self, blender_node_name: str, chain_data: dict):
        """Store conversion chain data for a node"""
        if chain_data:
            self.conversion_chains[blender_node_name] = chain_data


class ShaderGraphConverter:
    """Convert Blender shader graph to Unity format with advanced strategies"""
    
    def __init__(self, blender_shader_data: Dict, node_mapping: Dict):
        self.blender_data = blender_shader_data
        self.unity_graph = UnityShaderGraph(blender_shader_data['name'])
        self.node_guid_map = {}
        self.node_mapping = node_mapping  # Loaded from JSON
        self.conversion_warnings = []
        self.conversion_report = {
            'nodes_converted': 0,
            'nodes_decomposed': 0,
            'nodes_approximated': 0,
            'nodes_incompatible': 0,
            'connections_validated': 0,
            'type_mismatches': 0
        }

    def convert(self) -> UnityShaderGraph:
        """Perform full conversion with advanced strategies"""
        print("\n" + "="*70)
        print("BLENDER TO UNITY SHADER CONVERSION")
        print("="*70 + "\n")
        
        for node_data in self.blender_data['nodes']:
            self._convert_node(node_data)

        for conn in self.blender_data['connections']:
            self._convert_connection(conn)

        self._generate_conversion_report()
        
        return self.unity_graph

    def _convert_node(self, node_data: Dict):
        """Convert single Blender node with advanced strategies"""
        node_type = node_data['blender_type']
        guid = str(uuid.uuid4())
        self.node_guid_map[node_data['name']] = guid
        
        # Look up in JSON mapping
        node_mapping = self.node_mapping.get(node_type, {})
        strategy = node_mapping.get('strategy', 'incompatible')
        unity_name = node_mapping.get('unity_name', node_type)
        compat = node_mapping.get('compatibility', '0%')
        unity_chain = node_mapping.get('unity_chain', None)  # Get conversion steps from JSON
        
        if strategy == 'direct':
            node = self.unity_graph.add_node(unity_name, guid)
            node.properties = node_data['properties']
            node.conversion_chain = unity_chain  # Store conversion chain
            self.conversion_report['nodes_converted'] += 1
            print(f"✓ {node_data['name']:30} → {unity_name:25} [{compat}]")
        
        elif strategy == 'decompose':
            if node_type == 'ShaderNodeBsdfPrincipled':
                components = strategies.ConversionStrategy.handle_principled_bsdf(node_data)
                node = self.unity_graph.add_node('Custom (PBR)', guid)
                node.properties = components
                node.conversion_chain = unity_chain
                self.conversion_report['nodes_decomposed'] += 1
                print(f"⊕ {node_data['name']:30} → [5 PBR nodes]              [{compat}]")
        
        elif strategy == 'blend_mapping':
            blend_mode = node_data['properties'].get('blend_mode', 'MIX')
            formula = strategies.ConversionStrategy.handle_mix_rgb_blend_modes(blend_mode)
            node = self.unity_graph.add_node('Lerp', guid)
            node.properties = {'blend_formula': formula}
            node.conversion_chain = unity_chain
            self.conversion_report['nodes_approximated'] += 1
            print(f"≈ {node_data['name']:30} → Lerp                      [{compat}]")
        
        elif strategy == 'normal_mapping':
            conversion = strategies.ConversionStrategy.handle_normal_map(node_data)
            node = self.unity_graph.add_node('Normal From Texture', guid)
            node.properties = conversion
            node.conversion_chain = unity_chain
            self.conversion_report['nodes_converted'] += 1
            print(f"✓ {node_data['name']:30} → Normal From Texture       [{compat}]")
        
        elif strategy == 'texture_reference':
            node = self.unity_graph.add_node('Sample Texture 2D', guid)
            node.properties = node_data['properties']
            node.conversion_chain = unity_chain
            self.conversion_report['nodes_converted'] += 1
            print(f"✓ {node_data['name']:30} → Sample Texture 2D         [{compat}]")
        
        elif strategy == 'attribute_mapping':
            node = self.unity_graph.add_node('Vertex Attribute', guid)
            node.properties = node_data['properties']
            node.conversion_chain = unity_chain
            self.conversion_report['nodes_converted'] += 1
            print(f"✓ {node_data['name']:30} → Vertex Attribute          [{compat}]")
        
        elif strategy == 'uv_mapping':
            mapping = strategies.ConversionStrategy.handle_texture_mapping(node_data)
            node = self.unity_graph.add_node('Tiling and Offset', guid)
            node.properties = mapping
            node.conversion_chain = unity_chain
            self.conversion_report['nodes_converted'] += 1
            print(f"✓ {node_data['name']:30} → Tiling and Offset         [{compat}]")
        
        elif strategy == 'procedural_texture':
            # Handle procedural textures with chain from JSON
            node = self.unity_graph.add_node(unity_name, guid)
            node.properties = node_data['properties']
            node.conversion_chain = unity_chain
            self.conversion_report['nodes_approximated'] += 1
            print(f"≈ {node_data['name']:30} → {unity_name:25} [{compat}]")
        
        elif strategy == 'approximation':
            # Handle approximation nodes with chain from JSON
            node = self.unity_graph.add_node(unity_name, guid)
            node.properties = node_data['properties']
            node.conversion_chain = unity_chain
            self.conversion_report['nodes_approximated'] += 1
            print(f"≈ {node_data['name']:30} → {unity_name:25} [{compat}]")
        
        elif strategy == 'bake_only':
            # Nodes that need baking - include chain info for user
            node = self.unity_graph.add_node(unity_name, guid)
            node.properties = node_data['properties']
            node.conversion_chain = unity_chain
            self.conversion_report['nodes_incompatible'] += 1
            warning = f"BAKE REQUIRED: {node_data['name']} ({node_type}) - {unity_chain.get('description', 'See steps in JSON') if unity_chain else 'No conversion available'}"
            self.conversion_warnings.append(warning)
            print(f"✗ {node_data['name']:30} → BAKE REQUIRED           [{compat}]")
        
        elif strategy == 'incompatible':
            # Incompatible nodes - still store chain info for manual workarounds
            node = self.unity_graph.add_node(f'UNSUPPORTED: {node_type}', guid)
            node.conversion_chain = unity_chain
            self.conversion_report['nodes_incompatible'] += 1
            if unity_chain and unity_chain.get('steps'):
                warning = f"MANUAL: {node_data['name']} ({node_type}) - {unity_chain['steps'][0].get('note', 'See conversion steps in JSON')}"
            else:
                warning = f"MANUAL REVIEW: {node_data['name']} ({node_type})"
            self.conversion_warnings.append(warning)
            print(f"✗ {node_data['name']:30} → UNSUPPORTED               [{compat}]")
        
        else:
            node = self.unity_graph.add_node(f'UNSUPPORTED: {node_type}', guid)
            node.conversion_chain = unity_chain
            self.conversion_report['nodes_incompatible'] += 1
            warning = f"UNKNOWN STRATEGY: {node_data['name']} ({node_type})"
            self.conversion_warnings.append(warning)
            print(f"✗ {node_data['name']:30} → UNKNOWN STRATEGY         [{compat}]")

    def _convert_connection(self, conn: Dict):
        """Convert connection with advanced type checking"""
        from_guid = self.node_guid_map.get(conn['from_node'])
        to_guid = self.node_guid_map.get(conn['to_node'])
        
        if from_guid and to_guid:
            is_compat, method = socket_handler.SocketTypeHandler.check_compatibility(
                conn['from_type'], conn['to_type']
            )
            
            if is_compat:
                self.unity_graph.add_edge(from_guid, 0, to_guid, 0)
                self.conversion_report['connections_validated'] += 1
                
                if method != 'direct':
                    print(f"  ↔ {conn['from_node']:20} → {conn['to_node']:20} [{method}]")
            else:
                self.conversion_report['type_mismatches'] += 1
                warning = f"{conn['from_node']}.{conn['from_socket']} ({conn['from_type']}) → {conn['to_node']}.{conn['to_socket']} ({conn['to_type']})"
                self.conversion_warnings.append(warning)
                print(f"  ⚠ Type mismatch: {warning}")

    def _generate_conversion_report(self):
        """Generate diagnostics report"""
        print("\n" + "="*70)
        print("CONVERSION SUMMARY")
        print("="*70)
        print(f"Nodes converted (direct):     {self.conversion_report['nodes_converted']}")
        print(f"Nodes decomposed:             {self.conversion_report['nodes_decomposed']}")
        print(f"Nodes approximated:            {self.conversion_report['nodes_approximated']}")
        print(f"Nodes incompatible:           {self.conversion_report['nodes_incompatible']}")
        print(f"Connections validated:        {self.conversion_report['connections_validated']}")
        print(f"Type mismatches detected:     {self.conversion_report['type_mismatches']}")
        print("="*70 + "\n")
        
        if self.conversion_warnings:
            print("WARNINGS & REVIEW ITEMS:")
            for warning in self.conversion_warnings:
                print(f"  ⚠ {warning}")
            print()
        
        # Store conversion chains in the Unity graph for UI access
        self._store_conversion_chains()
    
    def _store_conversion_chains(self):
        """Store all conversion chain data in the Unity graph"""
        for node_data in self.blender_data['nodes']:
            node_type = node_data['blender_type']
            node_mapping = self.node_mapping.get(node_type, {})
            unity_chain = node_mapping.get('unity_chain', None)
            
            if unity_chain:
                self.unity_graph.add_conversion_chain(
                    node_data['name'], 
                    {
                        'blender_node': node_data['name'],
                        'blender_type': node_type,
                        'unity_name': node_mapping.get('unity_name', 'Unknown'),
                        'strategy': node_mapping.get('strategy', 'unknown'),
                        'compatibility': node_mapping.get('compatibility', '0%'),
                        'description': unity_chain.get('description', ''),
                        'steps': unity_chain.get('steps', []),
                        'blender_notes': unity_chain.get('blender_conversion_notes', '')
                    }
                )
