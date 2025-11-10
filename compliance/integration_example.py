"""
MAYA Node - Integration Example

This example demonstrates how to integrate the license enforcement system
into the MAYA Node controller.

License: BUSL-1.1 (converts to Apache 2.0 after 4 years)
"""

import time
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compliance.license_enforcement import (
    get_enforcer, 
    require_feature,
    LicenseStatus
)

# Mock classes for demonstration (would be real in production)
class SensorBus:
    def battery_soc(self): return 0.75
    def load_now(self): return 45.0
    def gen_now(self): return 60.0
    def reserve_kw(self): return 10.0
    def load_breakdown(self): return (20.0, 15.0, 10.0)  # P1, P2, P3
    def total_capacity_kw(self): return 150.0
    def irradiance_forecast(self, minutes): return [50, 55, 60]
    def load_forecast(self, minutes): return [40, 45, 50]

class ActuatorBus:
    def inverter_limit_kw(self): return 100.0
    def genset_kw(self): return 25.0
    def max_charge_kw(self): return 50.0
    def shed(self, tier): print(f"  → Shedding load tier {tier}")
    def start_genset(self, min_kw): print(f"  → Starting genset ({min_kw}kW)")
    def charge_battery(self, rate_kw): print(f"  → Charging battery ({rate_kw}kW)")
    def enable_all_loads(self): print(f"  → Enabling all loads")
    def defer(self, tier): print(f"  → Deferring load tier {tier}")
    def enable(self, tier): print(f"  → Enabling load tier {tier}")
    def idle_sleep(self, seconds): time.sleep(seconds)
    def limit_capacity(self, max_kw): print(f"  ⚠ Limiting capacity to {max_kw}kW")

class Safety:
    def __init__(self, sensors, actuators):
        self.s = sensors
        self.a = actuators
    
    def check_all(self):
        """Check all safety interlocks"""
        # Always enabled regardless of license
        pass


class PowerScheduler:
    """
    Enhanced PowerScheduler with license enforcement
    """
    
    def __init__(self, sensors, actuators):
        self.s = sensors
        self.a = actuators
        self.last_forecast = 0
        self.enforcer = get_enforcer()
        self.tick_count = 0
        
        # Validate license at startup
        self._validate_license_at_startup()
    
    def _validate_license_at_startup(self):
        """Validate license when scheduler starts"""
        print("\n" + "="*60)
        print("MAYA Node Power Scheduler - License Validation")
        print("="*60)
        
        status, message = self.enforcer.validate()
        info = self.enforcer.get_license_info()
        
        print(f"\nLicense ID: {info['license_id']}")
        print(f"Tier: {info['tier'].upper()}")
        print(f"Status: {info['status'].upper()}")
        print(f"Message: {message}")
        print(f"Max Capacity: {info['max_capacity_kw']}kW")
        print(f"Deployment: {info['deployment_type']}")
        
        if status == LicenseStatus.VALID:
            print("\n✓ License valid - full features enabled")
        elif status == LicenseStatus.GRACE_PERIOD:
            print("\n⚠ License expired but in grace period")
            print("  Please renew at portal.maya-node.example.com")
        elif status == LicenseStatus.EXPIRED:
            print("\n✗ License expired - running in safe mode")
            print("  Only critical safety features available")
        else:
            print("\n⚠ License issue detected")
        
        print("\nAvailable features:")
        for feature in info['features']:
            print(f"  • {feature}")
        print("="*60 + "\n")
    
    @require_feature("basic_forecasting")
    def update_forecasts(self):
        """
        Update basic forecasts (6-hour horizon)
        Available in: All tiers
        """
        if time.time() - self.last_forecast < 5:
            return
        
        self.gen_forecast = self.s.irradiance_forecast(6*60)
        self.load_forecast = self.s.load_forecast(6*60)
        self.last_forecast = time.time()
    
    @require_feature("extended_forecasting")
    def update_extended_forecasts(self):
        """
        Update extended forecasts (24-hour horizon)
        Available in: Professional, Enterprise
        """
        self.gen_forecast_24h = self.s.irradiance_forecast(24*60)
        self.load_forecast_24h = self.s.load_forecast(24*60)
        print("  → Extended 24h forecasting active")
    
    @require_feature("ml_optimization")
    def ml_optimize_dispatch(self):
        """
        ML-based optimization of dispatch strategy
        Available in: Enterprise only
        """
        # Advanced machine learning optimization
        print("  → ML optimization active")
    
    def dispatch(self):
        """
        Core dispatch logic (always available)
        """
        soc = self.s.battery_soc()
        p_load = self.s.load_now()
        p_gen = self.s.gen_now()
        reserve = self.s.reserve_kw()
        
        # Priority tiers: P1 critical, P2 important, P3 deferrable
        p1, p2, p3 = self.s.load_breakdown()
        headroom = p_gen + self.a.inverter_limit_kw() + self.a.genset_kw() - p1
        
        if soc < 0.15:  # brownout guard
            self.a.shed("P3")
            self.a.shed("P2")
            self.a.start_genset(min_kw=p1 + reserve)
        elif headroom >= (p2 + p3):
            self.a.charge_battery(rate_kw=min(headroom, self.a.max_charge_kw()))
            self.a.enable_all_loads()
        else:
            self.a.defer("P3")
            self.a.enable("P2")
            if soc < 0.35 and p_gen < p_load:
                self.a.start_genset(min_kw=p1 + p2 + reserve)
    
    def log_tick(self):
        """Log control loop tick"""
        self.tick_count += 1
        
        # Periodic capacity check (every hour)
        if self.tick_count % 14400 == 0:  # 14400 ticks = 1 hour at 250ms/tick
            self._check_capacity_compliance()
    
    def _check_capacity_compliance(self):
        """Check if deployment capacity is within license limits"""
        current_capacity = self.s.total_capacity_kw()
        is_valid, message = self.enforcer.enforce_capacity(current_capacity)
        
        if not is_valid:
            print(f"\n⚠ CAPACITY VIOLATION: {message}")
            print("  Please upgrade license or reduce system capacity")
            # Limit system capacity to licensed amount
            if self.enforcer.license.max_capacity_kw > 0:
                self.a.limit_capacity(self.enforcer.license.max_capacity_kw)


def main():
    """
    Main control loop with license enforcement
    """
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║         MAYA Node - Microgrid Controller                  ║")
    print("║         Integration Example with License Enforcement      ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    # Support custom license path via environment variable
    import compliance.license_enforcement as le
    if 'MAYA_LICENSE_FILE' in os.environ:
        le._enforcer = le.LicenseEnforcer(os.environ['MAYA_LICENSE_FILE'])
        le._enforcer.load_license()
    
    # Initialize license enforcer
    enforcer = get_enforcer()
    status, message = enforcer.validate()
    
    # Check if we can run
    if status == LicenseStatus.EXPIRED:
        print("\n✗ Cannot start: License expired beyond grace period")
        print("  System will run in safe mode with minimal features")
        print("  Please renew at portal.maya-node.example.com\n")
        return
    
    # Initialize components
    sensors = SensorBus()
    actuators = ActuatorBus()
    safety = Safety(sensors, actuators)
    scheduler = PowerScheduler(sensors, actuators)
    
    # Run control loop (demo: 3 iterations)
    print("\nStarting control loop (demo: 3 iterations)...\n")
    
    for i in range(3):
        print(f"Tick {i+1}:")
        
        # Safety checks (always run)
        safety.check_all()
        
        # Basic forecasting (available in all tiers)
        try:
            scheduler.update_forecasts()
            print("  → Basic 6h forecasting complete")
        except PermissionError as e:
            print(f"  ✗ {e}")
        
        # Extended forecasting (Professional+)
        try:
            scheduler.update_extended_forecasts()
        except PermissionError as e:
            print(f"  ⚠ Extended forecasting not available: {e}")
        
        # ML optimization (Enterprise only)
        try:
            scheduler.ml_optimize_dispatch()
        except PermissionError as e:
            print(f"  ⚠ ML optimization not available: {e}")
        
        # Core dispatch (always available)
        scheduler.dispatch()
        
        # Logging
        scheduler.log_tick()
        
        print()
        
        if i < 2:  # Don't sleep on last iteration
            actuators.idle_sleep(0.1)  # Shortened for demo
    
    print("="*60)
    print("Demo complete!")
    print("="*60 + "\n")
    
    # Show final license status
    info = enforcer.get_license_info()
    print("Final License Status:")
    print(f"  Tier: {info['tier']}")
    print(f"  Status: {info['status']}")
    print(f"  Features: {len(info['features'])} enabled")
    print()


if __name__ == "__main__":
    main()
