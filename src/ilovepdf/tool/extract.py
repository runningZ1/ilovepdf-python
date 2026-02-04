from __future__ import annotations

from ..task import Task


class Extract(Task):
    API_PARAMS = ["detailed"]

    def __init__(self, public_key: str, secret_key: str, make_start: bool = True) -> None:
        self.tool = "extract"
        self._detailed = False
        super().__init__(public_key, secret_key, make_start)

    @property
    def detailed(self) -> bool:
        return bool(self._detailed)

    @detailed.setter
    def detailed(self, value: bool) -> None:
        self._detailed = bool(value)
