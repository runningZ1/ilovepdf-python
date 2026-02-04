from __future__ import annotations

from typing import Any

import requests


class Response:
    def __init__(self, response: requests.Response) -> None:
        if not isinstance(response, requests.Response):
            raise ValueError("Argument must be of type 'requests.Response'")
        self.response = response
        self._body: Any = None

    @property
    def headers(self) -> dict:
        return dict(self.response.headers)

    @property
    def body(self) -> Any:
        if self._body is not None:
            return self._body
        content_type = self.response.headers.get("content-type", "")
        is_json = "application/json" in content_type.lower()
        if is_json:
            try:
                self._body = self.response.json()
            except ValueError:
                self._body = self.response.text
        else:
            self._body = self.response.text
        return self._body

    @property
    def raw_body(self) -> bytes:
        return self.response.content

    @property
    def code(self) -> int:
        return int(self.response.status_code)

    def success(self) -> bool:
        return str(self.response.status_code).startswith("2")
