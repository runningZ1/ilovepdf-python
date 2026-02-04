from __future__ import annotations

from typing import List

from ..element import Element
from ..errors import ArgumentEnumError, ArgumentError
from ..task import Task


class Watermark(Task):
    API_PARAMS = [
        "type",
        "mode",
        "text",
        "image",
        "pages",
        "gravity",
        "vertical_position",
        "horizontal_position",
        "vertical_adjustment_percent",
        "horizontal_adjustment_percent",
        "vertical_position_adjustment",
        "horizontal_position_adjustment",
        "mosaic",
        "rotation",
        "font_family",
        "font_style",
        "font_size",
        "font_color",
        "transparency",
        "layer",
        "elements",
    ]

    MODE_VALUES = ["image", "text", "multi"]
    TYPE_VALUES = ["image", "text"]
    GRAVITY_VALUES = [
        "North",
        "NorthEast",
        "NorthWest",
        "Center",
        "CenterEast",
        "CenterWest",
        "East",
        "West",
        "South",
        "SouthEast",
        "SouthWest",
    ]

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
    def type(self):
        return getattr(self, "_type", None)

    @type.setter
    def type(self, new_val: str) -> None:
        if new_val not in self.TYPE_VALUES:
            raise ArgumentEnumError(self.TYPE_VALUES)
        self._type = new_val
        if getattr(self, "_mode", None) is None:
            self._mode = new_val

    def _normalize_gravity(self, value: str) -> str:
        for allowed in self.GRAVITY_VALUES:
            if value.lower() == allowed.lower():
                return allowed
        raise ArgumentEnumError(self.GRAVITY_VALUES)

    @property
    def gravity(self):
        return getattr(self, "_gravity", None)

    @gravity.setter
    def gravity(self, new_val: str) -> None:
        self._gravity = self._normalize_gravity(new_val)

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

    @property
    def rotation(self):
        return getattr(self, "_rotation", None)

    @rotation.setter
    def rotation(self, new_val: int) -> None:
        if not isinstance(new_val, int) or not (0 <= new_val <= 360):
            raise ArgumentError("Rotation must be an integer between 0 and 360")
        self._rotation = new_val

    @property
    def rotate(self):
        return self.rotation

    @rotate.setter
    def rotate(self, new_val: int) -> None:
        self.rotation = new_val

    def extract_api_params(self):
        params = super().extract_api_params()
        params["elements"] = [element.to_api_hash() for element in self.elements]
        return params
