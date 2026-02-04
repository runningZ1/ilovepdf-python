from __future__ import annotations

from ..errors import ArgumentError
from .file_element import FileElement


class DateElement(FileElement):
    def __init__(self, file):
        super().__init__(file)
        self.type = "date"

    def date_format(self, value: str) -> None:
        if not isinstance(value, str):
            raise ArgumentError("value must be a String type of object")
        self.content = value
