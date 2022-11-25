import tkinter as tk

from automatic_door_control_system.core import Controller
from automatic_door_control_system.motion_sensor import Motion


class Simulator:
    def __init__(self, controller: Controller):
        self._controller = controller
        self._root = tk.Tk()
        self._root.title("Simulator")
        self._root.geometry("300x200")
        self._root.resizable(False, False)
        # display a button to change motion sensor
        approach_button = tk.Button(self._root, text="Approach", command=self._approach)
        approach_button.pack()
        leave_button = tk.Button(self._root, text="Leave", command=self._leave)
        leave_button.pack()
        # display a button to change infrared sensor
        place_object_button = tk.Button(self._root, text="Place object", command=self._place_object)
        place_object_button.pack()
        remove_object_button = tk.Button(
            self._root, text="Remove object", command=self._remove_object
        )
        remove_object_button.pack()
        # display a button to change physical resistance sensor
        block_door_button = tk.Button(self._root, text="Block door", command=self._block_door)
        block_door_button.pack()
        unblock_door_button = tk.Button(self._root, text="Unblock door", command=self._unblock_door)
        unblock_door_button.pack()

    @property
    def is_closed(self):
        try:
            return self._root.state() == "withdrawn"
        except tk.TclError:
            return True

    def _approach(self):
        self._controller.motion_sensor.detected_motion = Motion.APPROACHING

    def _leave(self):
        self._controller.motion_sensor.detected_motion = Motion.LEAVING

    def _place_object(self):
        self._controller.infrared_sensor.has_presence = True

    def _remove_object(self):
        self._controller.infrared_sensor.has_presence = False

    def _block_door(self):
        self._controller.physical_resistance_sensor.is_blocked = True

    def _unblock_door(self):
        self._controller.physical_resistance_sensor.is_blocked = False

    def update(self):
        self._root.update()

    def destroy(self):
        self._root.destroy()
