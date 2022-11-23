import unittest

from automatic_door_control_system.door import Door, DoorState
from automatic_door_control_system.motion_sensor import MotionSensor, Motion
from automatic_door_control_system.infrared_sensor import InfraredSensor
from automatic_door_control_system.physical_resistance_sensor import PhysicalResistanceSensor
from automatic_door_control_system.core import Controller


# FIXME asyncio issue
class TestController(unittest.TestCase):
    def test_controller(self):
        door = Door()
        motion_sensor = MotionSensor()
        infrared_sensor = InfraredSensor()
        physical_resistance_sensor = PhysicalResistanceSensor()
        controller = Controller(door, motion_sensor, infrared_sensor, physical_resistance_sensor)
        self.assertEqual(controller.door.state, DoorState.CLOSED)
        self.assertEqual(controller.motion_sensor.detected_motion, Motion.NONE)
        self.assertEqual(controller.infrared_sensor.has_presence, False)
        self.assertEqual(controller.physical_resistance_sensor.is_blocked, False)

    def test_controller_open_door(self):
        door = Door()
        motion_sensor = MotionSensor()
        infrared_sensor = InfraredSensor()
        physical_resistance_sensor = PhysicalResistanceSensor()
        controller = Controller(door, motion_sensor, infrared_sensor, physical_resistance_sensor)
        controller.motion_sensor.detected_motion = Motion.APPROACHING
        controller.update()
        self.assertEqual(controller.door.state, DoorState.OPENING)
        self.assertEqual(controller.motion_sensor.detected_motion, Motion.APPROACHING)

    def test_controller_close_door(self):
        door = Door()
        motion_sensor = MotionSensor()
        infrared_sensor = InfraredSensor()
        physical_resistance_sensor = PhysicalResistanceSensor()
        controller = Controller(door, motion_sensor, infrared_sensor, physical_resistance_sensor)
        controller.door.state = DoorState.OPEN
        controller._start_clear_time = 0
        controller.update()
        self.assertEqual(controller.door.state, DoorState.CLOSING)
