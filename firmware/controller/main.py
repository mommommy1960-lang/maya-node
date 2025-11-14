# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

from firmware.controller.scheduler import PowerScheduler
from firmware.controller.sensors import SensorBus
from firmware.controller.actuators import ActuatorBus
from firmware.controller.safety import Safety

def main():
    sensors = SensorBus()
    actuators = ActuatorBus()
    safety = Safety(sensors, actuators)
    scheduler = PowerScheduler(sensors, actuators)

    # 250 ms control loop
    while True:
        safety.check_all()             # trips, temps, smoke, arc-fault, ground
        scheduler.update_forecasts()   # irradiance, load, SOC trajectories
        scheduler.dispatch()           # set inverter setpoints, contactors
        scheduler.log_tick()           # local ring buffer + batch upload
        actuators.idle_sleep(0.25)

if __name__ == "__main__":
    main()
