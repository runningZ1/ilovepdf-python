from __future__ import annotations

from ilovepdf.task import Task


class Removebackgroundimage(Task):
    API_PARAMS = []

    def __init__(self, public_key: str, secret_key: str, make_start: bool = True) -> None:
        self.tool = "removebackgroundimage"
        super().__init__(public_key, secret_key, make_start)
