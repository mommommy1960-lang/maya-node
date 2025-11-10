"""
Stress Test: Resonance Suppression
Tests the MPRS fast loop's ability to handle resonance suppression under stress
"""

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from sim.mprs_fastloop import MPRSFastLoop


class TestResonanceSuppression:
    """Test suite for resonance suppression under stress conditions"""
    
    @pytest.fixture
    def fastloop_config(self):
        """Provide standard configuration for tests"""
        return {
            'resonance_threshold': 0.7,
            'suppression_factor': 2.0,
            'burst_detection_window': 50,
            'collapse_lock_timeout': 500,
            'telemetry_enabled': False
        }
    
    @pytest.fixture
    def fastloop(self, fastloop_config):
        """Create a fast loop instance"""
        return MPRSFastLoop(fastloop_config)
    
    def test_normal_operation(self, fastloop):
        """Test normal operation below threshold"""
        result = fastloop.process_tick(0.5)
        
        assert result['input_resonance'] == 0.5
        assert result['suppressed_resonance'] == 0.5
        assert result['collapsed'] is False
    
    def test_resonance_suppression(self, fastloop):
        """Test suppression when threshold is exceeded"""
        result = fastloop.process_tick(0.9)
        
        assert result['input_resonance'] == 0.9
        assert result['suppressed_resonance'] == 0.45  # 0.9 / 2.0
        assert result['collapsed'] is False
    
    def test_sustained_high_resonance(self, fastloop):
        """Test sustained high resonance values"""
        results = []
        for _ in range(100):
            result = fastloop.process_tick(0.8)
            results.append(result)
        
        # All values should be suppressed
        for result in results:
            assert result['suppressed_resonance'] < result['input_resonance']
    
    def test_stress_rapid_fluctuation(self, fastloop):
        """Test rapid fluctuation between high and low resonance"""
        results = []
        for i in range(1000):
            value = 0.9 if i % 2 == 0 else 0.3
            result = fastloop.process_tick(value)
            results.append(result)
        
        # Verify all ticks were processed
        assert len(results) == 1000
        
        # Check that suppression was applied to high values
        high_value_results = [r for r in results if r['input_resonance'] == 0.9]
        assert all(r['suppressed_resonance'] == 0.45 for r in high_value_results)
    
    def test_stress_continuous_high_load(self, fastloop):
        """Test continuous high resonance load"""
        results = []
        for _ in range(5000):
            result = fastloop.process_tick(0.95)
            results.append(result)
        
        # All should be suppressed
        assert all(r['suppressed_resonance'] < r['input_resonance'] for r in results)
        
        # Should trigger collapse after burst detection
        final_burst_count = results[-1]['burst_count']
        assert final_burst_count > 0
    
    def test_stress_extreme_values(self, fastloop):
        """Test extreme resonance values"""
        extreme_values = [0.0, 0.99, 1.0, 0.5, 0.75, 0.1]
        
        for value in extreme_values * 100:  # Repeat 100 times
            result = fastloop.process_tick(value)
            assert result['suppressed_resonance'] >= 0
            assert result['suppressed_resonance'] <= 1.0
    
    def test_reset_functionality(self, fastloop):
        """Test that reset clears state properly"""
        # Generate some state
        for _ in range(100):
            fastloop.process_tick(0.9)
        
        # Reset
        fastloop.reset()
        
        # Verify state is cleared
        assert len(fastloop.resonance_buffer) == 0
        assert len(fastloop.burst_events) == 0
        assert fastloop.collapsed_state is False
        assert fastloop.last_collapse_time is None
    
    def test_concurrent_stress_simulation(self, fastloop_config):
        """Test multiple fast loops running concurrently"""
        loops = [MPRSFastLoop(fastloop_config) for _ in range(10)]
        
        # Process ticks on all loops
        for _ in range(100):
            for loop in loops:
                result = loop.process_tick(0.85)
                assert result is not None
        
        # All loops should have independent state
        burst_counts = [loop.burst_events for loop in loops]
        # Verify they all processed independently
        assert all(isinstance(events, list) for events in burst_counts)
