from __future__ import annotations

from typing import Any, Iterable, Optional


class Error(Exception):
    pass


class ApiError(Error):
    def __init__(self, http_response: "Response", custom_msg: Optional[str] = None) -> None:
        msg_to_use = custom_msg if custom_msg else self._extract_error_text(http_response)
        super().__init__(msg_to_use)
        self.http_response = http_response

    def _extract_error_text(self, http_response: "Response") -> str:
        body = http_response.body
        title = "An error occurred"
        msg = "Check the response from the server"
        if isinstance(body, dict):
            if body.get("name"):
                title = body.get("name")
                msg = body.get("message")
            elif body.get("error"):
                err = body.get("error") or {}
                title = err.get("type")
                msg = err.get("message")
                if err.get("param"):
                    msg = f"{msg} Details: {err.get('param')}"
        return f"[{title}] {msg}"


class Errors:
    class AuthError(ApiError):
        pass

    class ProcessError(ApiError):
        pass

    class StartError(ApiError):
        pass

    class UploadError(ApiError):
        pass

    class DownloadError(ApiError):
        pass

    class ArgumentError(ValueError):
        pass

    class ArgumentEnumError(ArgumentError):
        def __init__(self, valid_values: Iterable[Any]) -> None:
            values = ", ".join(str(value) for value in valid_values)
            super().__init__(f"Provided argument is invalid. Valid values: {values}")

    class UnsupportedFunctionalityError(Error):
        pass


# Backwards-compatible names
AuthError = Errors.AuthError
ProcessError = Errors.ProcessError
StartError = Errors.StartError
UploadError = Errors.UploadError
DownloadError = Errors.DownloadError
ArgumentError = Errors.ArgumentError
ArgumentEnumError = Errors.ArgumentEnumError
UnsupportedFunctionalityError = Errors.UnsupportedFunctionalityError


from .response import Response  # noqa: E402
