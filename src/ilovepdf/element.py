from __future__ import annotations

from typing import Any, Dict

from .errors import ArgumentEnumError


class Element:
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

    VERTICAL_POSITION_VALUES = ["bottom", "middle", "top"]
    HORIZONTAL_POSITION_VALUES = ["left", "center", "right"]

    LAYER_VALUES = ["above", "below"]

    ATTR_DEFAULT_VALUES = {
        "type": "text",
        "mode": "text",
        "text": None,
        "image": None,
        "pages": "all",
        "vertical_position": "middle",
        "horizontal_position": "center",
        "vertical_adjustment": 0,
        "horizontal_adjustment": 0,
        "rotation": 0,
        "transparency": 100,
        "mosaic": False,
        "font_family": None,
        "font_style": "Regular",
        "font_color": "#000000",
        "font_size": 14,
        "image_resize": 1,
        "zoom": 1,
        "gravity": "center",
        "x_pos_percent": None,
        "y_pos_percent": None,
        "width_percent": None,
        "height_percent": None,
        "border": None,
        "layer": None,
        "bold": False,
        "server_filename": None,
    }

    def __init__(self, params: Dict[str, Any] | None = None) -> None:
        params = params or {}
        init_values = {**self.ATTR_DEFAULT_VALUES, **params}
        init_values = {k: v for k, v in init_values.items() if v is not None}
        for key, value in init_values.items():
            setattr(self, key, value)

    def _set_enum(self, value: str, allowed: list[str]) -> str:
        if value not in allowed:
            raise ArgumentEnumError(allowed)
        return value

    @property
    def font_family(self) -> str | None:
        return getattr(self, "_font_family", None)

    @font_family.setter
    def font_family(self, new_val: str) -> None:
        self._font_family = self._set_enum(new_val, self.FONT_FAMILY_VALUES)

    @property
    def layer(self) -> str | None:
        return getattr(self, "_layer", None)

    @layer.setter
    def layer(self, new_val: str) -> None:
        self._layer = self._set_enum(new_val, self.LAYER_VALUES)

    @property
    def vertical_position(self) -> str | None:
        return getattr(self, "_vertical_position", None)

    @vertical_position.setter
    def vertical_position(self, new_val: str) -> None:
        self._vertical_position = self._set_enum(new_val, self.VERTICAL_POSITION_VALUES)

    @property
    def horizontal_position(self) -> str | None:
        return getattr(self, "_horizontal_position", None)

    @horizontal_position.setter
    def horizontal_position(self, new_val: str) -> None:
        self._horizontal_position = self._set_enum(new_val, self.HORIZONTAL_POSITION_VALUES)

    def to_api_hash(self) -> Dict[str, Any]:
        export_hash: Dict[str, Any] = {}
        for key in self.ATTR_DEFAULT_VALUES.keys():
            value = getattr(self, key, None)
            if value is not None:
                export_hash[key] = value
        return export_hash
