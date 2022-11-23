from .sensor import Sensor


class PhysicalResistanceSensor(Sensor):
    name = "Physical Resistance Sensor"

    def __init__(self):
        super().__init__()
        self._is_blocked = False

    @property
    def is_blocked(self):
        return self._is_blocked

    @is_blocked.setter
    def is_blocked(self, value: bool):
        self._is_blocked = value

    def deactivate(self):
        self.is_blocked = False
        return super().deactivate()
