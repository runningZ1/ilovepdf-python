from __future__ import annotations

from ..errors import ArgumentError
from .file_element import FileElement


class InputElement(FileElement):
    def __init__(self, file, label: str, description: str | None = None):
        super().__init__(file)
        self.type = "input"
        self.label = label
        if description is not None:
            self.description = description

    def set_info(self, label: str = "", description: str | None = None) -> None:
        if label:
            self.label = label
        if description is not None:
            self.description = description

    @property
    def label(self) -> str | None:
        return self._label

    @label.setter
    def label(self, value: str) -> None:
        if not isinstance(value, str):
            raise ArgumentError("value must be a String type of object")
        self._label = value
        self.set_info_parameter("label", value)

    @property
    def description(self) -> str | None:
        return getattr(self, "_description", None)

    @description.setter
    def description(self, value: str) -> None:
        if not isinstance(value, str):
            raise ArgumentError("value must be a String type of object")
        self._description = value
        self.set_info_parameter("description", value)
