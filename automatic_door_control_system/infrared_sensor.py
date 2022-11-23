from .sensor import Sensor


class InfraredSensor(Sensor):
    name = "Infrared Sensor"

    def __init__(self):
        super().__init__()
        self._has_presence = False

    @property
    def has_presence(self):
        return self._has_presence

    @has_presence.setter
    def has_presence(self, value: bool):
        self._has_presence = value

    def deactivate(self):
        self.has_presence = False
        return super().deactivate()

    def __str__(self):
        return f"{self.name}: ({'Has presence' if self.has_presence else 'No presence'})"
