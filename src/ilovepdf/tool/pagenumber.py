from __future__ import annotations

from ..errors import ArgumentEnumError
from ..task import Task


class Pagenumber(Task):
    API_PARAMS = [
        "facing_pages",
        "first_cover",
        "pages",
        "starting_number",
        "vertical_position",
        "horizontal_position",
        "vertical_position_adjustment",
        "horizontal_position_adjustment",
        "font_family",
        "font_style",
        "font_size",
        "font_color",
        "text",
    ]

    VERTICAL_POSITION_VALUES = ["bottom", "middle", "top"]
    HORIZONTAL_POSITION_VALUES = ["left", "center", "right"]
    FONT_FAMILY_VALUES = [
        "Arial",
        "Arial Unicode MS",
        "Verdana",
        "Courier",
        "Times New Roman",
        "Comic Sans MS",
        "WenQuanYi Zen Hei",
        "Lohit Marathi",
    ]

    def __init__(self, public_key: str, secret_key: str, make_start: bool = True) -> None:
        self.tool = "pagenumber"
        super().__init__(public_key, secret_key, make_start)

    @property
    def vertical_position(self):
        return getattr(self, "_vertical_position", None)

    @vertical_position.setter
    def vertical_position(self, new_val: str) -> None:
        if new_val not in self.VERTICAL_POSITION_VALUES:
            raise ArgumentEnumError(self.VERTICAL_POSITION_VALUES)
        self._vertical_position = new_val

    @property
    def horizontal_position(self):
        return getattr(self, "_horizontal_position", None)

    @horizontal_position.setter
    def horizontal_position(self, new_val: str) -> None:
        if new_val not in self.HORIZONTAL_POSITION_VALUES:
            raise ArgumentEnumError(self.HORIZONTAL_POSITION_VALUES)
        self._horizontal_position = new_val

    @property
    def font_family(self):
        return getattr(self, "_font_family", None)

    @font_family.setter
    def font_family(self, new_val: str) -> None:
        if new_val not in self.FONT_FAMILY_VALUES:
            raise ArgumentEnumError(self.FONT_FAMILY_VALUES)
        self._font_family = new_val
