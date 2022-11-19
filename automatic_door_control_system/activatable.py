class Activatable:
    def __init__(self, activate=True):
        self._is_active = activate

    @property
    def is_active(self):
        return self._is_active

    def activate(self):
        self._is_active = True

    def deactivate(self):
        self._is_active = False
