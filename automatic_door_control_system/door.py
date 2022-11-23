import asyncio
from enum import Enum
from typing import Optional

from .activatable import Activatable


class DoorState(Enum):
    CLOSED = 1
    OPENING = 2
    OPEN = 3
    CLOSING = 4


class Door(Activatable):
    def __init__(self, open_close_time=2):
        super().__init__()
        self._open_close_time = open_close_time
        self._state = DoorState.CLOSED
        self._task: Optional[asyncio.Task] = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: DoorState):
        self._state = value

    async def _create_open_coroutine(self):
        self.state = DoorState.OPENING
        await asyncio.sleep(self._open_close_time)
        self.state = DoorState.OPEN

    async def _create_close_coroutine(self):
        self.state = DoorState.CLOSING
        await asyncio.sleep(self._open_close_time)
        self.state = DoorState.CLOSED

    def open(self):
        if self._task is not None:
            self._task.cancel()
        self._task = asyncio.create_task(self._create_open_coroutine())

    def close(self):
        if self._task is not None:
            self._task.cancel()
        self._task = asyncio.create_task(self._create_close_coroutine())
