import tkinter as tk

from automatic_door_control_system.core import Controller


class Monitor:
    def __init__(self, controller: Controller):
        self._controller = controller
        self._root = tk.Tk()
        self._root.title("Automatic Door Control System")
        self._root.geometry("300x200")
        self._root.resizable(False, False)
        # display door state
        self._door_state = tk.StringVar()
        self._door_state.set(controller.door)
        door_state_label = tk.Label(self._root, textvariable=self._door_state)
        door_state_label.pack()
        # display motion sensor state
        self._motion_sensor_states = tk.StringVar()
        self._motion_sensor_states.set(controller.motion_sensor)
        motion_sensor_states_label = tk.Label(self._root, textvariable=self._motion_sensor_states)
        motion_sensor_states_label.pack()
        # display infrared sensor state
        self._infrared_sensor_state = tk.StringVar()
        self._infrared_sensor_state.set(controller.infrared_sensor)
        infrared_sensor_state_label = tk.Label(self._root, textvariable=self._infrared_sensor_state)
        infrared_sensor_state_label.pack()
        # display physical resistance sensor state
        self._physical_resistance_sensor_state = tk.StringVar()
        self._physical_resistance_sensor_state.set(controller.physical_resistance_sensor)
        physical_resistance_sensor_state_label = tk.Label(
            self._root, textvariable=self._physical_resistance_sensor_state
        )
        physical_resistance_sensor_state_label.pack()

    def update(self):
        self._door_state.set(self._controller.door)
        self._motion_sensor_states.set(self._controller.motion_sensor)
        self._infrared_sensor_state.set(self._controller.infrared_sensor)
        self._physical_resistance_sensor_state.set(self._controller.physical_resistance_sensor)
        self._root.update()

    @property
    def is_closed(self):
        return self._root.state() == "withdrawn"
