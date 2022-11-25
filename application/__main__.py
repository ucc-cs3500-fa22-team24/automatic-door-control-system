import asyncio

from automatic_door_control_system.core import Controller
from automatic_door_control_system.door import Door
from automatic_door_control_system.infrared_sensor import InfraredSensor
from automatic_door_control_system.motion_sensor import MotionSensor
from automatic_door_control_system.physical_resistance_sensor import PhysicalResistanceSensor
from gui.monitor import Monitor
from gui.simulator import Simulator

door = Door()
motion_sensor = MotionSensor()
infrared_sensor = InfraredSensor()
physical_resistance_sensor = PhysicalResistanceSensor()

controller = Controller(door, motion_sensor, infrared_sensor, physical_resistance_sensor)

monitor = Monitor(controller)
simulator = Simulator(controller)


async def main():
    while True:
        if monitor.is_closed or simulator.is_closed:
            break
        await asyncio.sleep(0.1)
        controller.update()
        simulator.update()
        monitor.update()


if __name__ == "__main__":
    asyncio.run(main())
