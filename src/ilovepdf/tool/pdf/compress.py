from __future__ import annotations

from ...errors import ArgumentEnumError
from ...task import Task


class Compress(Task):
    API_PARAMS = ["compression_level"]
    COMPRESSION_LEVEL_VALUES = ["extreme", "recommended", "low"]

    def __init__(self, public_key: str, secret_key: str, make_start: bool = True) -> None:
        self.tool = "compress"
        self._compression_level = None
        super().__init__(public_key, secret_key, make_start)

    @property
    def compression_level(self):
        return self._compression_level

    @compression_level.setter
    def compression_level(self, level: str) -> None:
        if level not in self.COMPRESSION_LEVEL_VALUES:
            raise ArgumentEnumError(self.COMPRESSION_LEVEL_VALUES)
        self._compression_level = level
