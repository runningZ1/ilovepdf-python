from __future__ import annotations

from ...errors import ArgumentEnumError
from ...task import Task


class Imagepdf(Task):
    API_PARAMS = ["orientation", "margin", "pagesize", "merge_after"]

    ORIENTATION_VALUES = ["portrait", "landscape"]
    PAGESIZE_VALUES = ["fit", "A4", "letter"]

    def __init__(self, public_key: str, secret_key: str, make_start: bool = True) -> None:
        self.tool = "imagepdf"
        self.merge_after = True
        super().__init__(public_key, secret_key, make_start)

    @property
    def orientation(self):
        return getattr(self, "_orientation", None)

    @orientation.setter
    def orientation(self, new_val: str) -> None:
        if new_val not in self.ORIENTATION_VALUES:
            raise ArgumentEnumError(self.ORIENTATION_VALUES)
        self._orientation = new_val

    @property
    def pagesize(self):
        return getattr(self, "_pagesize", None)

    @pagesize.setter
    def pagesize(self, new_val: str) -> None:
        if new_val not in self.PAGESIZE_VALUES:
            raise ArgumentEnumError(self.PAGESIZE_VALUES)
        self._pagesize = new_val
