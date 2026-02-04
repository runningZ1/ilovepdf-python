from __future__ import annotations

from ...task import Task


class Pdfocr(Task):
    API_PARAMS = []

    def __init__(self, public_key: str, secret_key: str, make_start: bool = True) -> None:
        self.tool = "pdfocr"
        super().__init__(public_key, secret_key, make_start)
