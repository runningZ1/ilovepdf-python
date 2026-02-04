from __future__ import annotations

from ..errors import ArgumentEnumError, UnsupportedFunctionalityError
from ..task import Task


class ValidatePdfa(Task):
    API_PARAMS = ["conformance"]

    CONFORMANCE_VALUES = [
        "pdfa-1b",
        "pdfa-1a",
        "pdfa-2b",
        "pdfa-2u",
        "pdfa-2a",
        "pdfa-3b",
        "pdfa-3u",
        "pdfa-3a",
    ]

    def __init__(self, public_key: str, secret_key: str, make_start: bool = True) -> None:
        self.tool = "validatepdfa"
        self._conformance = None
        super().__init__(public_key, secret_key, make_start)

    @property
    def conformance(self) -> str:
        return self._conformance or "pdfa-2b"

    @conformance.setter
    def conformance(self, new_val: str) -> None:
        if new_val not in self.CONFORMANCE_VALUES:
            raise ArgumentEnumError(self.CONFORMANCE_VALUES)
        self._conformance = new_val

    def download_file(self):
        raise UnsupportedFunctionalityError("This tool does not download files (Check in the sample files how to use it)")
