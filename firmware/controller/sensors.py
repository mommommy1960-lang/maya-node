# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

"""
Sensor Bus Interface

Provides interface to read sensor data from the microgrid system.
"""

class SensorBus:
    """
    Interface to sensor subsystems.
    
    Provides readings for:
    - Battery state of charge
    - Power generation
    - Load consumption
    - Environmental sensors
    """
    
    def __init__(self):
        """Initialize sensor bus."""
        # TODO: Initialize actual sensor interfaces
        pass
    
    def battery_soc(self) -> float:
        """
        Get battery state of charge.
        
        Returns:
            SOC as fraction (0.0 to 1.0)
        """
        # TODO: Read from battery management system
        return 0.8  # Placeholder
    
    def load_now(self) -> float:
        """
        Get current load power.
        
        Returns:
            Load in kW
        """
        # TODO: Read from power meters
        return 10.0  # Placeholder
    
    def gen_now(self) -> float:
        """
        Get current generation power.
        
        Returns:
            Generation in kW
        """
        # TODO: Read from generation meters
        return 15.0  # Placeholder
    
    def reserve_kw(self) -> float:
        """
        Get required power reserve.
        
        Returns:
            Reserve in kW
        """
        # TODO: Calculate from system requirements
        return 2.0  # Placeholder
    
    def load_breakdown(self) -> tuple:
        """
        Get load breakdown by priority tier.
        
        Returns:
            Tuple of (P1, P2, P3) loads in kW
        """
        # TODO: Read from load classification
        return (5.0, 3.0, 2.0)  # Placeholder
    
    def irradiance_forecast(self, horizon_minutes: int) -> list:
        """
        Get solar irradiance forecast.
        
        Args:
            horizon_minutes: Forecast horizon in minutes
            
        Returns:
            List of forecasted irradiance values
        """
        # TODO: Implement forecasting
        return [0.8] * (horizon_minutes // 15)  # Placeholder
    
    def load_forecast(self, horizon_minutes: int) -> list:
        """
        Get load forecast.
        
        Args:
            horizon_minutes: Forecast horizon in minutes
            
        Returns:
            List of forecasted load values in kW
        """
        # TODO: Implement forecasting
        return [10.0] * (horizon_minutes // 15)  # Placeholder
