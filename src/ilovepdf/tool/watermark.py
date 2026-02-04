from __future__ import annotations

from typing import List

from ..element import Element
from ..errors import ArgumentEnumError, ArgumentError
from ..task import Task


class Watermark(Task):
    API_PARAMS = [
        "mode",
        "text",
        "image",
        "pages",
        "vertical_position",
        "horizontal_position",
        "vertical_position_adjustment",
        "horizontal_position_adjustment",
        "mosaic",
        "rotate",
        "font_family",
        "font_style",
        "font_size",
        "font_color",
        "transparency",
        "layer",
        "elements",
    ]

    MODE_VALUES = ["image", "text", "multi"]

    def __init__(self, public_key: str, secret_key: str, make_start: bool = True) -> None:
        self.tool = "watermark"
        self._elements: List[Element] = []
        super().__init__(public_key, secret_key, make_start)

    @property
    def elements(self) -> List[Element]:
        return self._elements

    def add_element(self, element: Element) -> None:
        if not isinstance(element, Element):
            raise ArgumentError("Element must be of type 'Ilovepdf::Element'")
        self._elements.append(element)

    @property
    def mode(self):
        return getattr(self, "_mode", None)

    @mode.setter
    def mode(self, new_val: str) -> None:
        if new_val not in self.MODE_VALUES:
            raise ArgumentEnumError(self.MODE_VALUES)
        self._mode = new_val

    @property
    def vertical_position(self):
        return getattr(self, "_vertical_position", None)

    @vertical_position.setter
    def vertical_position(self, new_val: str) -> None:
        if new_val not in Element.VERTICAL_POSITION_VALUES:
            raise ArgumentEnumError(Element.VERTICAL_POSITION_VALUES)
        self._vertical_position = new_val

    @property
    def horizontal_position(self):
        return getattr(self, "_horizontal_position", None)

    @horizontal_position.setter
    def horizontal_position(self, new_val: str) -> None:
        if new_val not in Element.HORIZONTAL_POSITION_VALUES:
            raise ArgumentEnumError(Element.HORIZONTAL_POSITION_VALUES)
        self._horizontal_position = new_val

    @property
    def font_family(self):
        return getattr(self, "_font_family", None)

    @font_family.setter
    def font_family(self, new_val: str) -> None:
        if new_val not in Element.FONT_FAMILY_VALUES:
            raise ArgumentEnumError(Element.FONT_FAMILY_VALUES)
        self._font_family = new_val

    @property
    def layer(self):
        return getattr(self, "_layer", None)

    @layer.setter
    def layer(self, new_val: str) -> None:
        if new_val not in Element.LAYER_VALUES:
            raise ArgumentEnumError(Element.LAYER_VALUES)
        self._layer = new_val

    def extract_api_params(self):
        params = super().extract_api_params()
        params["elements"] = [element.to_api_hash() for element in self.elements]
        return params
