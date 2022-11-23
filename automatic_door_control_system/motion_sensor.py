from enum import Enum

from .sensor import Sensor


class Motion(Enum):
    NONE = 0
    APPROACHING = 1
    LEAVING = 2


class MotionSensor(Sensor):
    name = "Motion Sensor"

    def __init__(self):
        super().__init__()
        self._detected_motion = Motion.NONE

    @property
    def detected_motion(self):
        return self._detected_motion

    @detected_motion.setter
    def detected_motion(self, motion: Motion):
        self._detected_motion = motion

    def deactivate(self):
        self.detected_motion = Motion.NONE
        return super().deactivate()
