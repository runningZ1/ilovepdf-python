from __future__ import annotations

from ...errors import ArgumentEnumError
from ...task import Task


class Resize(Task):
    API_PARAMS = [
        "resize_mode",
        "pixels_width",
        "pixels_height",
        "percentage",
        "maintain_ratio",
        "no_enlarge_if_smaller",
    ]

    RESIZE_MODE_VALUES = ["pixels", "percentage"]

    def __init__(self, public_key: str, secret_key: str, make_start: bool = True) -> None:
        self.tool = "resizeimage"
        self._resize_mode = None
        super().__init__(public_key, secret_key, make_start)

    @property
    def resize_mode(self):
        return self._resize_mode

    @resize_mode.setter
    def resize_mode(self, mode: str) -> None:
        if mode not in self.RESIZE_MODE_VALUES:
            raise ArgumentEnumError(self.RESIZE_MODE_VALUES)
        self._resize_mode = mode
