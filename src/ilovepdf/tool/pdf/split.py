from __future__ import annotations

from ...task import Task


class Split(Task):
    API_PARAMS = ["ranges", "split_mode", "fixed_range", "remove_pages", "merge_after"]

    def __init__(self, public_key: str, secret_key: str, make_start: bool = True) -> None:
        self.tool = "split"
        self._merge_after = False
        self._split_mode = None
        self._fixed_range = None
        self._remove_pages = None
        self._ranges = None
        super().__init__(public_key, secret_key, make_start)

    @property
    def merge_after(self):
        return getattr(self, "_merge_after", False)

    @merge_after.setter
    def merge_after(self, value: bool) -> None:
        self._merge_after = value

    @property
    def split_mode(self):
        return self._split_mode

    @split_mode.setter
    def split_mode(self, value: str) -> None:
        self._split_mode = value

    @property
    def fixed_range(self):
        return self._fixed_range

    @fixed_range.setter
    def fixed_range(self, value: int) -> None:
        self._split_mode = "fixed_range"
        self._fixed_range = value

    @property
    def remove_pages(self):
        return self._remove_pages

    @remove_pages.setter
    def remove_pages(self, pages: str) -> None:
        self._split_mode = "remove_pages"
        self._remove_pages = pages

    @property
    def ranges(self):
        return self._ranges

    @ranges.setter
    def ranges(self, pages: str) -> None:
        self._split_mode = "ranges"
        self._ranges = pages
