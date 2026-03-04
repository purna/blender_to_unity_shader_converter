"""
Conversion Strategies
Implementations for complex node conversions
"""

from typing import Dict, Any

class ConversionStrategy:
    """Detailed conversion strategies for complex node types"""
    
    @staticmethod
    def handle_principled_bsdf(node_data: Dict) -> Dict:
        """
        Decompose Principled BSDF into PBR components
        """
        base_color = node_data['inputs'].get('Base Color', {}).get('default')
        metallic = node_data['inputs'].get('Metallic', {}).get('default', 0.0)
        roughness = node_data['inputs'].get('Roughness', {}).get('default', 0.5)
        normal = node_data['inputs'].get('Normal')
        emission = node_data['inputs'].get('Emission', {}).get('default')
        ior = node_data['inputs'].get('IOR', {}).get('default', 1.45)
        
        components = {
            'base_color': base_color,
            'metallic': float(metallic) if metallic else 0.0,
            'roughness': max(0.05, min(1.0, float(roughness))) if roughness else 0.5,
            'normal': normal,
            'emission': emission,
            'ior': float(ior) if ior else 1.45
        }
        
        print(f"  → Decomposing Principled BSDF into {len(components)} components")
        return components

    @staticmethod
    def handle_mix_rgb_blend_modes(blend_mode: str) -> str:
        """
        Map Blender blend modes to Unity approximations
        """
        blend_map = {
            'MIX': 'Lerp(Color1, Color2, Factor)',
            'MULTIPLY': 'Multiply(Color1, Color2)',
            'SCREEN': '1 - (1 - Color1) * (1 - Color2)',
            'OVERLAY': 'Conditional blend (complex)',
            'HARD_LIGHT': 'Switch-based blend',
            'ADD': 'Add(Color1, Color2)',
            'SUBTRACT': 'Subtract(Color1, Color2)',
            'DIVIDE': 'Divide(Color1, Color2)',
            'LIGHTEN': 'Max(Color1, Color2)',
            'DARKEN': 'Min(Color1, Color2)',
        }
        
        formula = blend_map.get(blend_mode, f'Lerp (fallback for {blend_mode})')
        print(f"  → Blend mode '{blend_mode}' → {formula}")
        return formula

    @staticmethod
    def handle_normal_map(node_data: Dict) -> Dict:
        """
        Normal map color space conversion strategy
        """
        height_input = node_data['inputs'].get('Height')
        strength = node_data['inputs'].get('Strength', {}).get('default', 1.0)
        
        conversion = {
            'input': height_input,
            'strength': float(strength) if strength else 1.0,
            'strategy': 'Sample → Separate RGB → [Flip G if DirectX] → Normal From Texture',
            'note': 'Detect texture color space in source image properties'
        }
        
        print(f"  → Normal map conversion: strength={conversion['strength']}")
        return conversion

    @staticmethod
    def handle_bump_map(node_data: Dict) -> Dict:
        """
        Bump map height-to-normal conversion
        """
        height_input = node_data['inputs'].get('Height')
        strength = node_data['inputs'].get('Strength', {}).get('default', 1.0)
        distance = node_data['inputs'].get('Distance', {}).get('default', 1.0)
        
        strategy = {
            'method': 'Height→Normal approximation',
            'parameters': {
                'height': height_input,
                'strength': float(strength) if strength else 1.0,
                'distance': float(distance) if distance else 1.0
            }
        }
        
        print(f"  → Bump map: height→normal with strength {strategy['parameters']['strength']}")
        return strategy

    @staticmethod
    def handle_texture_mapping(node_data: Dict) -> Dict:
        """
        Map UV transforms directly
        """
        location = node_data['properties'].get('location', (0, 0, 0))
        rotation = node_data['properties'].get('rotation', (0, 0, 0))
        scale = node_data['properties'].get('scale', (1, 1, 1))
        
        mapping = {
            'offset': location[:2] if location else (0, 0),
            'tiling': scale[:2] if scale else (1, 1),
            'rotation': rotation[2] if rotation else 0,
            'note': 'Copy Location→Offset, Scale→Tiling, Rotation[Z]→Rotation'
        }
        
        print(f"  → Texture mapping: scale={mapping['tiling']}, offset={mapping['offset']}")
        return mapping
