"""
MPRS Fast Loop Simulation
Multi-Party Resonance Suppression fast-loop simulation engine
"""

import time
import json
from typing import Dict, List, Optional


class MPRSFastLoop:
    """Fast-loop simulation for MPRS operations"""
    
    def __init__(self, config: Dict):
        """Initialize the MPRS fast loop with configuration
        
        Args:
            config: Configuration dictionary matching mprs_inputs.schema.json
        """
        self.resonance_threshold = config.get('resonance_threshold', 0.5)
        self.suppression_factor = config.get('suppression_factor', 1.0)
        self.burst_detection_window = config.get('burst_detection_window', 100)
        self.collapse_lock_timeout = config.get('collapse_lock_timeout', 1000)
        self.telemetry_enabled = config.get('telemetry_enabled', False)
        
        self.resonance_buffer: List[float] = []
        self.burst_events: List[Dict] = []
        self.collapsed_state = False
        self.last_collapse_time: Optional[float] = None
    
    def process_tick(self, resonance_value: float) -> Dict:
        """Process a single simulation tick
        
        Args:
            resonance_value: Current resonance measurement
            
        Returns:
            Dictionary containing tick results
        """
        timestamp = time.time()
        
        # Add to resonance buffer
        self.resonance_buffer.append(resonance_value)
        if len(self.resonance_buffer) > self.burst_detection_window:
            self.resonance_buffer.pop(0)
        
        # Check for resonance threshold breach
        suppressed_value = resonance_value
        if resonance_value > self.resonance_threshold:
            suppressed_value = resonance_value / self.suppression_factor
            
        # Check for burst conditions
        if len(self.resonance_buffer) >= self.burst_detection_window:
            avg_resonance = sum(self.resonance_buffer) / len(self.resonance_buffer)
            if avg_resonance > self.resonance_threshold * 1.5:
                self.burst_events.append({
                    'timestamp': timestamp,
                    'avg_resonance': avg_resonance
                })
        
        # Check collapse lock conditions
        if self.last_collapse_time:
            time_since_collapse = (timestamp - self.last_collapse_time) * 1000
            if time_since_collapse < self.collapse_lock_timeout:
                self.collapsed_state = True
            else:
                self.collapsed_state = False
                self.last_collapse_time = None
        
        # Trigger collapse if conditions met
        if len(self.burst_events) > 3 and not self.collapsed_state:
            self.collapsed_state = True
            self.last_collapse_time = timestamp
        
        result = {
            'timestamp': timestamp,
            'input_resonance': resonance_value,
            'suppressed_resonance': suppressed_value,
            'collapsed': self.collapsed_state,
            'burst_count': len(self.burst_events)
        }
        
        if self.telemetry_enabled:
            self._log_telemetry(result)
        
        return result
    
    def _log_telemetry(self, data: Dict):
        """Log telemetry data"""
        # Placeholder for telemetry logging
        pass
    
    def reset(self):
        """Reset the fast loop state"""
        self.resonance_buffer.clear()
        self.burst_events.clear()
        self.collapsed_state = False
        self.last_collapse_time = None
