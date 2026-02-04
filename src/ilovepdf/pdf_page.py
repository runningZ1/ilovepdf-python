from __future__ import annotations


class PdfPage:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    @classmethod
    def from_string(cls, value: str) -> "PdfPage":
        width_str, height_str = value.split("x")
        return cls(float(width_str), float(height_str))
