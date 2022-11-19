from time import time

from activatable import Activatable
from door import DoorState
from motion_sensor import Motion


class Controller(Activatable):
    def __init__(self, door, motion_sensor, infrared_sensor, physical_resistance_sensor):
        super().__init__()
        self._door = door
        self._motion_sensor = motion_sensor
        self._infrared_sensor = infrared_sensor
        self._physical_resistance_sensor = physical_resistance_sensor
        self._start_clear_time = None

    @property
    def door_state(self):
        return self._door.state

    @property
    def motion_sensor_state(self):
        return self._motion_sensor.detected_motion

    @property
    def infrared_sensor_state(self):
        return self._infrared_sensor.has_presence

    @property
    def physical_resistance_sensor_state(self):
        return self._physical_resistance_sensor.is_blocked

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
            self._motion_sensor.detected_motion != Motion.APPROACHING
            and not self._infrared_sensor.has_presence
        ):
            if self._start_clear_time is None:
                self._start_clear_time = time()
            else:
                if time() - self._start_clear_time > 4:
                    self._door.close()
                    self._start_clear_time = None
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
