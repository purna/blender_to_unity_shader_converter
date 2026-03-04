"""
Socket Type Handler
Manages socket type compatibility and conversions
"""

from typing import Tuple

class SocketTypeHandler:
    """Handle socket type conversions and compatibility checking"""
    
    # Compatibility matrix: (from_type, to_type) -> conversion_method
    COMPATIBILITY_MATRIX = {
        ('RGBA', 'COLOR'): 'direct',
        ('COLOR', 'RGBA'): 'direct',
        ('VALUE', 'FLOAT'): 'direct',
        ('FLOAT', 'VALUE'): 'direct',
        ('VECTOR', 'VECTOR'): 'direct',
        ('SHADER', 'SHADER'): 'direct',
        
        # Cross-type conversions
        ('VALUE', 'VECTOR'): 'append_node',      # Replicate value across XYZ
        ('VECTOR', 'VALUE'): 'split_node',       # Extract single channel
        ('FLOAT', 'VECTOR'): 'append_node',
        ('VECTOR', 'FLOAT'): 'split_node',
        ('COLOR', 'VECTOR'): 'direct',           # RGB as XYZ
        ('VECTOR', 'COLOR'): 'direct',           # XYZ as RGB
    }
    
    @classmethod
    def check_compatibility(cls, from_type: str, to_type: str) -> Tuple[bool, str]:
        """
        Check if socket types are compatible
        
        Returns: (is_compatible, method_or_error)
        """
        key = (from_type, to_type)
        
        if key in cls.COMPATIBILITY_MATRIX:
            method = cls.COMPATIBILITY_MATRIX[key]
            return True, method
        
        if from_type == to_type:
            return True, 'direct'
        
        return False, f'No conversion for {from_type} → {to_type}'
    
    @staticmethod
    def get_all_conversions():
        """Get list of all supported conversions"""
        return list(SocketTypeHandler.COMPATIBILITY_MATRIX.keys())
