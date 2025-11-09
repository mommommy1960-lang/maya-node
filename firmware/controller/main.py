from scheduler import PowerScheduler
from sensors import SensorBus
from actuators import ActuatorBus
from safety import Safety

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
