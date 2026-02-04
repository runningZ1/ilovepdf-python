from __future__ import annotations

from ..errors import ArgumentError
from .file_element import FileElement


class TextElement(FileElement):
    def __init__(self, file, text: str):
        super().__init__(file)
        self.type = "text"
        self.content = text

    def set_content(self, value: str) -> None:
        if not isinstance(value, str):
            raise ArgumentError("value must be a String type of object")
        self.content = value
