# Firmware Controller

Edge controller firmware for MAYA Node microgrid management.

## Purpose

Provides real-time control for:
- Power scheduling and dispatch
- Battery management
- Load prioritization and shedding
- Generator control
- Safety monitoring

## Components

- `main.py` - Main control loop (250ms cycle)
- `scheduler.py` - Power scheduling and forecasting
- `sensors.py` - Sensor bus interface
- `actuators.py` - Actuator bus interface
- `safety.py` - Safety monitoring and protection

## Architecture

The controller runs a fast control loop (250ms) that:

1. **Safety Checks**: Monitor all safety-critical parameters
2. **Update Forecasts**: Update irradiance and load predictions
3. **Dispatch**: Make control decisions based on SOC, generation, and load
4. **Log**: Record telemetry to local buffer and cloud

## Priority Tiers

Loads are classified into priority tiers:

- **P1 (Critical)**: Essential loads that must stay powered
- **P2 (Important)**: Important loads, shed only in emergency
- **P3 (Deferrable)**: Deferrable loads, shed first during constraints

## Safety Features

- Temperature monitoring
- Smoke detection
- Arc-fault detection
- Ground fault detection
- Emergency shutdown sequences
- Brownout protection (SOC < 15%)

## Configuration

TODO: Add configuration file format and loading

## Testing

See `/firmware/edge-tests/` for simulation and testing tools.

## License

CERL-1.0 - See LICENSE-CERL-1.0 in repository root.
