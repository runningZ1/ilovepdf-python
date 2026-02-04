from __future__ import annotations

from typing import List

from ..errors import ArgumentError
from .file_element import FileElement


class Receiver:
    ALLOWED_TYPES = {"signer", "validator", "viewer"}

    def __init__(self, receiver_type: str, name: str, email: str, phone: str | None = None) -> None:
        self._elements: List[FileElement] = []
        self.type = receiver_type
        self.name = name
        self.email = email
        self.phone = phone
        self.access_code: str | None = None
        self.force_signature_type: str | None = None

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str) or not value:
            raise ArgumentError("Only String type of object is allowed")
        self._name = value

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        if not isinstance(value, str) or not value:
            raise ArgumentError("Only String type of object is allowed")
        self._email = value

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str) -> None:
        if value not in self.ALLOWED_TYPES:
            raise ArgumentError(f"type is not valid, valid types are: {', '.join(self.ALLOWED_TYPES)}")
        self._type = value

    @property
    def phone(self) -> str | None:
        return getattr(self, "_phone", None)

    @phone.setter
    def phone(self, value: str | None) -> None:
        if value is not None and not isinstance(value, str):
            raise ArgumentError("Only String type of object is allowed")
        self._phone = value

    def set_access_code(self, value: str) -> None:
        if not isinstance(value, str):
            raise ArgumentError("Only String type of object is allowed")
        self.access_code = value

    def set_force_signature_type(self, value: str) -> None:
        if not isinstance(value, str):
            raise ArgumentError("Only String type of object is allowed")
        self.force_signature_type = value

    @property
    def elements(self) -> List[FileElement]:
        return self._elements

    def add_element(self, element: FileElement) -> List[FileElement]:
        if not isinstance(element, FileElement):
            raise ArgumentError("Only Ilovepdf::Signature::FileElement type of object is allowed")
        self._elements.append(element)
        return self._elements

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "type": self.type,
            "access_code": self.access_code,
            "force_signature_type": self.force_signature_type,
            "files": self._files_to_list(),
        }

    def _files_to_list(self):
        grouped = {}
        for element in self._elements:
            grouped.setdefault(element.file.server_filename, []).append(element)
        result = []
        for server_filename, elements in grouped.items():
            result.append(
                {
                    "server_filename": server_filename,
                    "elements": [element.to_dict() for element in elements],
                }
            )
        return result
