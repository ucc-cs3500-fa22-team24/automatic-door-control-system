import asyncio
from enum import Enum
from time import time
from typing import Optional, Coroutine

from .activatable import Activatable


class DoorState(Enum):
    CLOSED = 1
    OPENING = 2
    OPEN = 3
    CLOSING = 4


class Door(Activatable):
    DEFAULT_OPEN_CLOSE_TIME = 2

    def __init__(self, open_close_time=DEFAULT_OPEN_CLOSE_TIME):
        super().__init__()
        self._open_close_time = open_close_time
        self._state = DoorState.CLOSED
        self._transition_start_time: Optional[float] = None
        self._task: Optional[asyncio.Task] = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: DoorState):
        self._state = value
        if value == DoorState.OPENING or value == DoorState.CLOSING:
            self._transition_start_time = time()
        else:
            self._transition_start_time = None

    def _get_transition_pass_time(self):
        if self._transition_start_time is None:
            return self._open_close_time
        transition_past_time = time() - self._transition_start_time
        return min(transition_past_time, self._open_close_time)

    async def _create_open_coroutine(self):
        transition_pass_time = self._get_transition_pass_time()
        self.state = DoorState.OPENING
        await asyncio.sleep(transition_pass_time)
        self.state = DoorState.OPEN

    async def _create_close_coroutine(self):
        transition_pass_time = self._get_transition_pass_time()
        self.state = DoorState.CLOSING
        await asyncio.sleep(transition_pass_time)
        self.state = DoorState.CLOSED

    def _create_task(self, coroutine: Coroutine):
        if self._task is not None:
            self._task.cancel()
        self._task = asyncio.create_task(coroutine)
        self._task.add_done_callback(lambda _: setattr(self, "_task", None))

    def open(self):
        self._create_task(self._create_open_coroutine())

    def close(self):
        self._create_task(self._create_close_coroutine())

    def __str__(self):
        return f"Door: ({self.state.name})"
