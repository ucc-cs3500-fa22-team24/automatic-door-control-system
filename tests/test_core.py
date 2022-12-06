import asyncio
import unittest

from automatic_door_control_system.core import Controller
from automatic_door_control_system.door import Door, DoorState
from automatic_door_control_system.infrared_sensor import InfraredSensor
from automatic_door_control_system.motion_sensor import MotionSensor, Motion
from automatic_door_control_system.physical_resistance_sensor import PhysicalResistanceSensor


class TestController(unittest.IsolatedAsyncioTestCase):
    async def test_controller(self):
        door = Door()
        motion_sensor = MotionSensor()
        infrared_sensor = InfraredSensor()
        physical_resistance_sensor = PhysicalResistanceSensor()
        controller = Controller(door, motion_sensor, infrared_sensor, physical_resistance_sensor)
        self.assertEqual(DoorState.CLOSED, controller.door.state)
        self.assertEqual(Motion.NONE, controller.motion_sensor.detected_motion)
        self.assertEqual(False, controller.infrared_sensor.has_presence)
        self.assertEqual(False, controller.physical_resistance_sensor.is_blocked)

    async def test_controller_open_door(self):
        door = Door()
        motion_sensor = MotionSensor()
        infrared_sensor = InfraredSensor()
        physical_resistance_sensor = PhysicalResistanceSensor()
        controller = Controller(door, motion_sensor, infrared_sensor, physical_resistance_sensor)
        controller.motion_sensor.detected_motion = Motion.APPROACHING
        controller.update()
        await asyncio.sleep(0)
        self.assertEqual(DoorState.OPENING, controller.door.state)
        self.assertEqual(Motion.APPROACHING, controller.motion_sensor.detected_motion)
        await asyncio.sleep(Door.DEFAULT_OPEN_CLOSE_TIME)
        self.assertEqual(DoorState.OPEN, controller.door.state)

    async def test_controller_close_door(self):
        door = Door()
        motion_sensor = MotionSensor()
        infrared_sensor = InfraredSensor()
        physical_resistance_sensor = PhysicalResistanceSensor()
        controller = Controller(door, motion_sensor, infrared_sensor, physical_resistance_sensor)
        controller.door.state = DoorState.OPEN
        controller._doorway_clear_start_time = 0
        controller.update()
        await asyncio.sleep(0)
        self.assertEqual(DoorState.CLOSING, controller.door.state)
        await asyncio.sleep(Door.DEFAULT_OPEN_CLOSE_TIME)
        self.assertEqual(DoorState.CLOSED, controller.door.state)
