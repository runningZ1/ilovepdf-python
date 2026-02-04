from __future__ import annotations

import json
from typing import Any, Dict

from ..errors import ArgumentError
from ..file import File


class FileElement:
    def __init__(self, file: File) -> None:
        if not isinstance(file, File):
            raise ArgumentError("Only Ilovepdf::File type of object is allowed")
        self.file = file
        self.position = "0 0"
        self.pages = "1"
        self.size = 40
        self._info: Dict[str, Any] | None = None
        self.type: str | None = None
        self.content: Any = None

    def set_position(self, x: float = 0, y: float = 0) -> str:
        if not isinstance(x, (int, float)):
            raise ArgumentError("x must be an integer or float")
        if not isinstance(y, (int, float)):
            raise ArgumentError("y must be an integer or float")
        self.position = f"{abs(x)} {-abs(y)}"
        return self.position

    def set_info_parameter(self, parameter_name: str, value: Any) -> Dict[str, Any]:
        if self._info is None:
            self._info = {}
        self._info[parameter_name] = value
        return self._info

    @property
    def info(self) -> str | None:
        if self._info is None:
            return None
        return json.dumps(self._info)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "position": self.position,
            "pages": self.pages,
            "size": self.size,
            "info": self.info,
            "type": self.type,
            "content": self.content,
        }

    @property
    def pages(self) -> str:
        return self._pages

    @pages.setter
    def pages(self, value: str) -> None:
        if not isinstance(value, str):
            raise ArgumentError("value must be string type")
        self._pages = value

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, value: int) -> None:
        if not isinstance(value, int):
            raise ArgumentError("value must be Integer type")
        self._size = value
