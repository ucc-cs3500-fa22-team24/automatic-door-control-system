from time import time
from typing import Optional

from .activatable import Activatable
from .door import DoorState, Door
from .infrared_sensor import InfraredSensor
from .motion_sensor import Motion, MotionSensor
from .physical_resistance_sensor import PhysicalResistanceSensor


class Controller(Activatable):
    DOORWAY_CLEAR_TIME = 4

    def __init__(
        self,
        door: Door,
        motion_sensor: MotionSensor,
        infrared_sensor: InfraredSensor,
        physical_resistance_sensor: PhysicalResistanceSensor,
    ):
        super().__init__()
        self._door = door
        self._motion_sensor = motion_sensor
        self._infrared_sensor = infrared_sensor
        self._physical_resistance_sensor = physical_resistance_sensor
        self._doorway_clear_start_time: Optional[float] = None

    @property
    def door(self):
        return self._door

    @property
    def motion_sensor(self):
        return self._motion_sensor

    @property
    def infrared_sensor(self):
        return self._infrared_sensor

    @property
    def physical_resistance_sensor(self):
        return self._physical_resistance_sensor

    def update(self):
        if not self.is_active:
            return
        # door is closed
        if self._door.state == DoorState.CLOSED and (
            self._motion_sensor.detected_motion == Motion.APPROACHING
        ):
            self._door.open()
        # door is open
        elif self._door.state == DoorState.OPEN and (
            not self._motion_sensor.detected_motion == Motion.APPROACHING
            and not self._infrared_sensor.has_presence
        ):
            if self._doorway_clear_start_time is None:
                self._doorway_clear_start_time = time()
            else:
                if time() - self._doorway_clear_start_time > self.DOORWAY_CLEAR_TIME:
                    self._door.close()
                    self._doorway_clear_start_time = None
        # door is closing
        elif self._door.state == DoorState.CLOSING and (
            self._motion_sensor.detected_motion == Motion.APPROACHING
            or self._infrared_sensor.has_presence
            or self._physical_resistance_sensor.is_blocked
        ):
            self._door.open()

    def deactivate(self):
        self._door.deactivate()
        self._motion_sensor.deactivate()
        self._infrared_sensor.deactivate()
        return super().deactivate()
