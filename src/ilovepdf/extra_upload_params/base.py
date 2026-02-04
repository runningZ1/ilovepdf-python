from __future__ import annotations

from typing import Any, Dict


class Base:
    def __init__(self) -> None:
        self.extra_params: Dict[str, Any] = {}

    def set_value(self, key: str, value: Any) -> None:
        self.extra_params[key] = value

    def get_values(self) -> Dict[str, Any]:
        return dict(self.extra_params)
