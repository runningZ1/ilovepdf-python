from __future__ import annotations

from ...errors import ArgumentEnumError
from ...task import Task


class Htmlpdf(Task):
    API_PARAMS = ["page_orientation", "page_margin", "page_size"]

    PAGE_ORIENTATION_VALUES = ["portrait", "landscape"]
    PAGE_SIZE_VALUES = ["A3", "A4", "A5", "A6", "Letter"]

    def __init__(self, public_key: str, secret_key: str, make_start: bool = True) -> None:
        self.tool = "htmlpdf"
        super().__init__(public_key, secret_key, make_start)

    @property
    def page_orientation(self) -> str | None:
        return getattr(self, "_page_orientation", None)

    @page_orientation.setter
    def page_orientation(self, new_val: str) -> None:
        if new_val not in self.PAGE_ORIENTATION_VALUES:
            raise ArgumentEnumError(self.PAGE_ORIENTATION_VALUES)
        self._page_orientation = new_val

    @property
    def page_size(self) -> str | None:
        return getattr(self, "_page_size", None)

    @page_size.setter
    def page_size(self, new_val: str) -> None:
        if new_val not in self.PAGE_SIZE_VALUES:
            raise ArgumentEnumError(self.PAGE_SIZE_VALUES)
        self._page_size = new_val
