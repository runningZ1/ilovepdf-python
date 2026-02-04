from __future__ import annotations

from ...task import Task
from ..pdf.watermark import Watermark


class Watermarkimage(Watermark):
    def __init__(self, public_key: str, secret_key: str, make_start: bool = True) -> None:
        self.tool = "watermarkimage"
        self._elements = []
        Task.__init__(self, public_key, secret_key, make_start)

    def extract_api_params(self):
        allowed_keys = {
            "type",
            "text",
            "image",
            "gravity",
            "x_pos_percent",
            "y_pos_percent",
            "width_percent",
            "height_percent",
            "vertical_adjustment_percent",
            "horizontal_adjustment_percent",
            "rotation",
            "transparency",
            "mosaic",
            "font_family",
            "font_style",
            "font_size",
            "font_color",
        }
        gravity_map = {
            "north": (50, 0),
            "northeast": (100, 0),
            "northwest": (0, 0),
            "center": (50, 50),
            "centereast": (100, 50),
            "centerwest": (0, 50),
            "east": (100, 50),
            "west": (0, 50),
            "south": (50, 100),
            "southeast": (100, 100),
            "southwest": (0, 100),
        }
        elements_payload = []
        for element in self.elements:
            raw = element.to_api_hash()
            data = {k: v for k, v in raw.items() if k in allowed_keys and v is not None}
            if data.get("x_pos_percent") is None or data.get("y_pos_percent") is None:
                gravity = data.get("gravity")
                if isinstance(gravity, str):
                    pos = gravity_map.get(gravity.replace(" ", "").lower())
                    if pos:
                        data.setdefault("x_pos_percent", pos[0])
                        data.setdefault("y_pos_percent", pos[1])
            if data.get("width_percent") is None:
                data["width_percent"] = 30
            if data.get("height_percent") is None:
                data["height_percent"] = 10
            elements_payload.append(data)
        return {"elements": elements_payload}
