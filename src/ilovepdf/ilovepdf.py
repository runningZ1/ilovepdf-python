from __future__ import annotations

import secrets
import time
from typing import Any, Dict, Optional, Tuple

import jwt
import requests

from .errors import ApiError, Error, Errors
from .helper import camelize_str, underscore_str
from .request_payload.form_url_encoded import FormUrlEncoded
from .response import Response
from .servers import START_SERVER


class Ilovepdf:
    START_SERVER = START_SERVER
    API_VERSION = "python.v1"
    TOKEN_ALGORITHM = "HS256"
    ALL_ENDPOINTS = ["start", "upload", "process", "download", "task"]
    LONG_JOB_ENDPOINTS = ["process", "upload", "download"]
    TIME_DELAY = 5400

    _raise_exceptions = False

    def __init__(self, public_key: Optional[str] = None, secret_key: Optional[str] = None) -> None:
        self.set_api_keys(public_key, secret_key)
        self.api_version = self.API_VERSION
        self.encrypt_key: Optional[str] = None
        self.debug = False
        self.timeout = 10
        self.long_timeout: Optional[int] = None
        self._token: Optional[str] = None
        self._worker_server: Optional[str] = None

    @classmethod
    def raise_exceptions(cls, value: bool) -> None:
        cls._raise_exceptions = bool(value)

    @classmethod
    def raise_exceptions_enabled(cls) -> bool:
        return cls._raise_exceptions is True

    def set_api_keys(self, public_key: Optional[str], secret_key: Optional[str]) -> None:
        self._public_key = public_key
        self._secret_key = secret_key

    def new_task(self, tool_name: str, make_start: bool = True):
        from . import tool as tool_module

        tool_name_str = str(tool_name)
        camelized_name = camelize_str(tool_name_str)
        task_class = getattr(tool_module, camelized_name, None)
        if not task_class:
            normalized = tool_name_str.replace("-", "_")
            for class_name, klass in tool_module.TOOL_CLASSES.items():
                if underscore_str(class_name) == normalized:
                    task_class = klass
                    break
        if not task_class:
            raise Error(
                f"Unknown tool '{tool_name}'. Available tools: {self.all_tool_names()}"
            )
        return task_class(self._public_key, self._secret_key, make_start)

    @classmethod
    def all_tool_names(cls):
        from . import tool as tool_module

        return [underscore_str(name) for name in tool_module.TOOL_CLASSES.keys()]

    def enable_file_encryption(self, enable: bool, new_encrypt_key: Optional[str] = None) -> None:
        if enable:
            if new_encrypt_key and len(new_encrypt_key) not in (16, 24, 32):
                raise ValueError("Encryption key must be 16, 24 or 32 characters long")
            self.encrypt_key = new_encrypt_key or secrets.token_hex(16)
        else:
            self.encrypt_key = None

    def send_request(self, http_method: str, endpoint: str, extra_opts: Optional[Dict[str, Any]] = None) -> Response:
        extra_opts = extra_opts or {}
        body = extra_opts.get("body", {})
        headers = dict(extra_opts.get("headers", {}))

        headers["Accept"] = "application/json"
        headers["Authorization"] = f"Bearer {self._jwt()}"

        if self.debug and isinstance(body, dict):
            body["debug"] = True

        server = self.worker_server or self.START_SERVER
        request_uri = f"{server}/v1/{endpoint}"

        endpoint_base = endpoint.split("/", 1)[0]
        timeout_to_use = self.long_timeout if endpoint_base in self.LONG_JOB_ENDPOINTS and self.long_timeout else self.timeout

        method = http_method.lower()
        files = None
        data = None

        if isinstance(body, dict) and body.pop("multipart", False):
            files, data = self._prepare_multipart(body)
        elif isinstance(body, dict):
            encoded = FormUrlEncoded(body).extract_to_str()
            if method in ("get", "delete"):
                if encoded:
                    request_uri = self._append_query(request_uri, encoded)
            else:
                data = encoded
                headers.setdefault("Content-Type", FormUrlEncoded.mime_type)
        elif isinstance(body, str):
            if method in ("get", "delete"):
                if body:
                    request_uri = self._append_query(request_uri, body)
            else:
                data = body
                headers.setdefault("Content-Type", FormUrlEncoded.mime_type)

        try:
            response = requests.request(
                method,
                request_uri,
                headers=headers,
                data=data,
                files=files,
                timeout=timeout_to_use,
            )
        except requests.RequestException as exc:
            raise Error(str(exc)) from exc
        wrapped = Response(response)

        if response.status_code == 401:
            raise Errors.AuthError(wrapped)
        if not wrapped.success():
            raise self._klass_error_for(endpoint_base)(wrapped)
        return wrapped

    def query_task_status(self, new_server: str, task_id: str) -> Response:
        old_server = self.worker_server
        self.worker_server = new_server
        try:
            response = self.send_request("get", f"task/{task_id}")
        finally:
            self.worker_server = old_server
        return response

    @property
    def worker_server(self) -> Optional[str]:
        return self._worker_server

    @worker_server.setter
    def worker_server(self, new_server: Optional[str]) -> None:
        self._worker_server = new_server

    def _jwt(self) -> str:
        if not self._api_keys_present():
            raise Error("You must provide a set of API keys")
        payload = self._jwt_token_payload()
        self._token = jwt.encode(payload, self._secret_key, algorithm=self.TOKEN_ALGORITHM)
        return self._token

    def _api_keys_present(self) -> bool:
        return bool(self._public_key and self._secret_key)

    def _klass_error_for(self, endpoint_base: str):
        mapping = {
            "start": Errors.StartError,
            "upload": Errors.UploadError,
            "process": Errors.ProcessError,
            "download": Errors.DownloadError,
        }
        return mapping.get(endpoint_base, ApiError)

    def _jwt_token_payload(self) -> Dict[str, Any]:
        current_time = int(time.time())
        params = {
            "iss": "",
            "aud": "",
            "iat": current_time - self.TIME_DELAY,
            "nbf": current_time - self.TIME_DELAY,
            "exp": current_time + 3600 + self.TIME_DELAY,
            "jti": self._public_key,
        }
        if self._is_file_encrypted():
            params["file_encryption_key"] = self.encrypt_key
        return params

    def _is_file_encrypted(self) -> bool:
        return self.encrypt_key is not None

    def _append_query(self, url: str, query: str) -> str:
        return f"{url}&{query}" if "?" in url else f"{url}?{query}"

    def _prepare_multipart(self, body: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        data: Dict[str, Any] = {}
        files: Dict[str, Any] = {}
        for key, value in body.items():
            if hasattr(value, "read"):
                files[key] = value
            else:
                data[key] = value
        return files, data
