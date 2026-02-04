from __future__ import annotations

from ..task import Task


class Pdfjpg(Task):
    API_PARAMS = [
        "view_width",
        "view_height",
        "navigation_timeout",
        "delay",
        "page_size",
        "page_orientation",
        "page_margin",
        "remove_popups",
        "single_page",
    ]

    PAGE_SIZE_VALUES = ["A3", "A4", "A5", "A6", "Letter"]
    PAGE_ORIENTATION_VALUES = ["portrait", "landscape"]

    def __init__(self, public_key: str, secret_key: str, make_start: bool = True) -> None:
        self.tool = "pdfjpg"
        super().__init__(public_key, secret_key, make_start)
        self.view_width = 1920
        self.navigation_timeout = 10
        self.delay = 2
        self.page_margin = 0

    def add_url(self, file_url: str):
        return self.add_file_from_url(file_url)
