"""
Visibility Minimizer Module

This module implements strategies for minimizing external visibility
while maintaining internal operational transparency.
"""

import hashlib
from typing import Dict, List, Optional


class VisibilityMinimizer:
    """
    Manages visibility levels for different operational aspects.
    """
    
    def __init__(self):
        self.visibility_map = {}
        self.obfuscation_level = "standard"
    
    def set_visibility(self, entity_id: str, level: str) -> None:
        """
        Set visibility level for an entity.
        
        Args:
            entity_id: Identifier for the entity
            level: Visibility level (hidden, minimal, standard, full)
        """
        valid_levels = ["hidden", "minimal", "standard", "full"]
        if level not in valid_levels:
            raise ValueError(f"Invalid visibility level: {level}")
        
        self.visibility_map[entity_id] = level
    
    def obfuscate_identifier(self, identifier: str) -> str:
        """
        Obfuscate an identifier for external presentation.
        
        Args:
            identifier: Original identifier
            
        Returns:
            str: Obfuscated identifier
        """
        hash_obj = hashlib.sha256(identifier.encode())
        return hash_obj.hexdigest()[:16]
    
    def filter_sensitive_data(self, data: Dict) -> Dict:
        """
        Filter sensitive data based on visibility settings.
        
        Args:
            data: Original data dictionary
            
        Returns:
            Dict: Filtered data with sensitive fields removed or obfuscated
        """
        filtered = {}
        sensitive_fields = ["private_key", "seed", "password", "internal_id"]
        
        for key, value in data.items():
            if key in sensitive_fields:
                filtered[key] = "***REDACTED***"
            else:
                filtered[key] = value
        
        return filtered
    
    def generate_public_view(self, internal_data: Dict) -> Dict:
        """
        Generate a public-safe view of internal data.
        
        Args:
            internal_data: Internal data structure
            
        Returns:
            Dict: Public-safe representation
        """
        public_data = {}
        allowed_fields = ["status", "timestamp", "type"]
        
        for field in allowed_fields:
            if field in internal_data:
                public_data[field] = internal_data[field]
        
        return public_data
    
    def apply_noise(self, value: float, noise_level: float = 0.05) -> float:
        """
        Apply statistical noise to obfuscate exact values.
        
        Args:
            value: Original value
            noise_level: Proportion of noise to add (0.0 to 1.0)
            
        Returns:
            float: Value with applied noise
        """
        import random
        noise = value * noise_level * (random.random() - 0.5) * 2
        return value + noise
