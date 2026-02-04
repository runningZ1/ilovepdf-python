from __future__ import annotations

from ilovepdf.errors import ArgumentEnumError
from ilovepdf.task import Task


class Upscaleimage(Task):
    API_PARAMS = ["multiplier"]
    MULTIPLIER_VALUES = [2, 4]

    def __init__(self, public_key: str, secret_key: str, make_start: bool = True) -> None:
        self.tool = "upscaleimage"
        self._multiplier = None
        super().__init__(public_key, secret_key, make_start)

    @property
    def multiplier(self):
        return self._multiplier

    @multiplier.setter
    def multiplier(self, new_val: int) -> None:
        if new_val not in self.MULTIPLIER_VALUES:
            raise ArgumentEnumError(self.MULTIPLIER_VALUES)
        self._multiplier = new_val
