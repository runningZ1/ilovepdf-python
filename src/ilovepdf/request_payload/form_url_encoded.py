from __future__ import annotations

from typing import Any, Dict, List
from urllib.parse import quote_plus


class FormUrlEncoded:
    mime_type = "application/x-www-form-urlencoded"

    def __init__(self, body: Dict[str, Any]) -> None:
        if not isinstance(body, dict):
            raise ValueError("Body must be a dict")
        self.body = body

    def extract_to_str(self) -> str:
        components: List[str] = []
        for key, value in self.body.items():
            resolved = self._stringify(key, value)
            if resolved:
                components.append(resolved)
        return "&".join(components)

    def _stringify(self, key: str, value: Any) -> str | None:
        components: List[str] = []
        if isinstance(value, dict):
            if not value:
                return None
            for hk, hv in value.items():
                prop_name = quote_plus(str(hk))
                resolved = self._stringify(f"{key}[{prop_name}]", hv)
                if resolved:
                    components.append(resolved)
        elif isinstance(value, list):
            if not value:
                return None
            for idx, item in enumerate(value):
                resolved = self._stringify(f"{key}[{idx}]", item)
                if resolved:
                    components.append(resolved)
        else:
            if value is None:
                return None
            resolved = f"{key}=" + quote_plus(str(value))
            components.append(resolved)
        return "&".join(components)
