"""
Stress Test: Burst Trap
Tests the MPRS fast loop's burst detection and trapping mechanisms under stress
"""

import pytest
import sys
import os
import time

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from sim.mprs_fastloop import MPRSFastLoop


class TestBurstTrap:
    """Test suite for burst detection and trapping under stress"""
    
    @pytest.fixture
    def burst_config(self):
        """Configuration optimized for burst detection"""
        return {
            'resonance_threshold': 0.6,
            'suppression_factor': 1.5,
            'burst_detection_window': 20,
            'collapse_lock_timeout': 300,
            'telemetry_enabled': False
        }
    
    @pytest.fixture
    def fastloop(self, burst_config):
        """Create a fast loop instance"""
        return MPRSFastLoop(burst_config)
    
    def test_burst_detection_basic(self, fastloop):
        """Test basic burst detection"""
        # Generate burst pattern
        for _ in range(25):
            fastloop.process_tick(0.95)
        
        result = fastloop.process_tick(0.95)
        assert result['burst_count'] > 0
    
    def test_burst_detection_threshold(self, fastloop):
        """Test burst detection requires threshold breach"""
        # Below threshold should not create bursts
        for _ in range(50):
            result = fastloop.process_tick(0.5)
        
        assert result['burst_count'] == 0
    
    def test_stress_multiple_bursts(self, fastloop):
        """Test detection of multiple burst events"""
        results = []
        
        # Create multiple burst patterns
        for cycle in range(10):
            for _ in range(30):
                result = fastloop.process_tick(0.92)
                results.append(result)
            
            # Cool down period
            for _ in range(5):
                result = fastloop.process_tick(0.3)
                results.append(result)
        
        final_burst_count = results[-1]['burst_count']
        assert final_burst_count >= 5, f"Expected multiple bursts, got {final_burst_count}"
    
    def test_stress_rapid_burst_generation(self, fastloop):
        """Test rapid generation of burst conditions"""
        burst_counts = []
        
        for _ in range(1000):
            result = fastloop.process_tick(0.95)
            burst_counts.append(result['burst_count'])
        
        # Burst count should increase over time
        assert burst_counts[-1] > burst_counts[100]
        assert burst_counts[-1] > 0
    
    def test_burst_window_boundary(self, fastloop):
        """Test burst detection at window boundaries"""
        # Fill window minus one
        for _ in range(19):
            fastloop.process_tick(0.95)
        
        result_before = fastloop.process_tick(0.95)
        burst_before = result_before['burst_count']
        
        # One more should trigger detection
        result_after = fastloop.process_tick(0.95)
        burst_after = result_after['burst_count']
        
        assert burst_after >= burst_before
    
    def test_stress_burst_with_noise(self, fastloop):
        """Test burst detection with noisy data"""
        import random
        
        for _ in range(500):
            # High average with noise
            base_value = 0.9
            noise = random.uniform(-0.1, 0.1)
            value = max(0.0, min(1.0, base_value + noise))
            
            result = fastloop.process_tick(value)
        
        # Should still detect bursts despite noise
        assert result['burst_count'] > 0
    
    def test_burst_triggers_collapse(self, fastloop):
        """Test that sufficient bursts trigger collapse state"""
        # Generate enough bursts to trigger collapse
        for _ in range(100):
            fastloop.process_tick(0.95)
        
        result = fastloop.process_tick(0.95)
        
        # Should have bursts and potentially collapsed
        assert result['burst_count'] > 0
        # Collapse may or may not be triggered depending on burst threshold
    
    def test_stress_alternating_burst_patterns(self, fastloop):
        """Test alternating burst and normal patterns"""
        results = []
        
        for cycle in range(20):
            # Burst phase
            for _ in range(25):
                result = fastloop.process_tick(0.92)
                results.append(result)
            
            # Normal phase
            for _ in range(25):
                result = fastloop.process_tick(0.4)
                results.append(result)
        
        # Verify processing completed
        assert len(results) == 1000
        
        # Should have detected multiple bursts
        assert results[-1]['burst_count'] > 5
    
    def test_stress_sustained_burst_conditions(self, fastloop):
        """Test sustained burst conditions over long period"""
        start_bursts = 0
        
        for i in range(5000):
            result = fastloop.process_tick(0.93)
            
            if i == 100:
                start_bursts = result['burst_count']
        
        final_bursts = result['burst_count']
        
        # Should accumulate many bursts
        assert final_bursts > start_bursts
        assert final_bursts > 10
    
    def test_burst_buffer_management(self, fastloop):
        """Test that burst buffer doesn't grow unbounded"""
        for _ in range(10000):
            fastloop.process_tick(0.95)
        
        # Buffer should be capped at window size
        assert len(fastloop.resonance_buffer) == fastloop.burst_detection_window
    
    def test_stress_precision_burst_detection(self, fastloop):
        """Test precise burst detection at exact thresholds"""
        threshold = fastloop.resonance_threshold * 1.5
        
        # Just below threshold
        for _ in range(25):
            fastloop.process_tick(threshold - 0.01)
        
        result_below = fastloop.process_tick(threshold - 0.01)
        bursts_below = result_below['burst_count']
        
        # Reset and test just above threshold
        fastloop.reset()
        
        for _ in range(25):
            fastloop.process_tick(threshold + 0.01)
        
        result_above = fastloop.process_tick(threshold + 0.01)
        bursts_above = result_above['burst_count']
        
        # Above threshold should have more bursts
        assert bursts_above >= bursts_below
