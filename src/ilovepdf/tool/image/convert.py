from __future__ import annotations

from ...task import Task


class Convert(Task):
    API_PARAMS = [
        "to",
        "gif_time",
        "gif_loop",
    ]

    def __init__(self, public_key: str, secret_key: str, make_start: bool = True) -> None:
        self.tool = "convertimage"
        super().__init__(public_key, secret_key, make_start)
