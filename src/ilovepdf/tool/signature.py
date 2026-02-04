from __future__ import annotations

from typing import Any, Dict, List

from ..errors import ArgumentError, UnsupportedFunctionalityError
from ..file import File
from ..request_payload.form_url_encoded import FormUrlEncoded
from ..task import Task
from ..signature.receiver import Receiver


class Signature(Task):
    API_PARAMS = [
        "brand_name",
        "brand_logo",
        "language",
        "lock_order",
        "message_signer",
        "subject_signer",
        "uuid_visible",
        "expiration_days",
        "signer_reminders",
        "signer_reminder_days_cycle",
        "verify_enabled",
    ]

    def __init__(self, public_key: str, secret_key: str, make_start: bool = True) -> None:
        self.tool = "sign"
        self._signers: List[Receiver] = []
        super().__init__(public_key, secret_key, make_start)

    def execute(self):
        self._result = self.send_to_sign()
        return self._result

    @property
    def uuid_visible(self) -> bool:
        return bool(getattr(self, "_uuid_visible", False))

    @uuid_visible.setter
    def uuid_visible(self, value: bool) -> None:
        self._uuid_visible = bool(value)

    @property
    def brand_name(self):
        return getattr(self, "_brand_name", None)

    @brand_name.setter
    def brand_name(self, value: str) -> None:
        raise UnsupportedFunctionalityError("Method not implemented")

    @property
    def brand_logo(self):
        return getattr(self, "_brand_logo", None)

    @brand_logo.setter
    def brand_logo(self, value: str) -> None:
        raise UnsupportedFunctionalityError("Method not implemented")

    def add_receiver(self, receiver: Receiver) -> None:
        if not isinstance(receiver, Receiver):
            raise ArgumentError("value is not receiver")
        self._signers.append(receiver)

    @property
    def language(self):
        return getattr(self, "_language", None)

    @language.setter
    def language(self, value: str) -> None:
        if not isinstance(value, str):
            raise ArgumentError("value is not a string")
        self._language = value

    @property
    def lock_order(self):
        return getattr(self, "_lock_order", None)

    @lock_order.setter
    def lock_order(self, value: bool) -> None:
        self._lock_order = "1" if bool(value) else "0"

    def email_content(self, subject: str, body: str) -> Dict[str, str]:
        self.subject_signer = subject
        self.message_signer = body
        return {"subject": self.subject_signer, "body": self.message_signer}

    @property
    def expiration_days(self):
        return getattr(self, "_expiration_days", None)

    @expiration_days.setter
    def expiration_days(self, value: int) -> None:
        if not isinstance(value, int):
            raise ArgumentError("value is not an Integer")
        self._expiration_days = value

    def reminders(self, value: int) -> int:
        if not isinstance(value, int):
            raise ArgumentError("value is not an Integer")
        if value <= 0:
            self.signer_reminders = False
            self.signer_reminder_days_cycle = None
        else:
            self.signer_reminders = True
            self.signer_reminder_days_cycle = value
        return value

    def upload_brand_logo_file(self, logo_path: str):
        return self.perform_upload_request(logo_path)

    def upload_brand_logo_file_from_url(self, logo_url: str):
        return self.perform_upload_url_request(logo_url)

    def add_brand(self, name: str, logo: File):
        self._brand_logo = logo.server_filename
        self._brand_name = name

    @property
    def verify_enabled(self):
        return bool(getattr(self, "_verify_enabled", False))

    @verify_enabled.setter
    def verify_enabled(self, value: bool) -> None:
        self._verify_enabled = bool(value)

    @property
    def signers(self) -> List[Receiver]:
        return self._signers

    def __lshift__(self, receiver: Receiver):
        if not isinstance(receiver, Receiver):
            raise ArgumentError("value is not an Ilovepdf::Signature::Receiver")
        self._signers.append(receiver)
        return self

    def extract_api_params(self) -> Dict[str, Any]:
        params = super().extract_api_params()
        params["task"] = self.task_id
        params["files"] = [
            {"server_filename": file.server_filename, "filename": file.filename}
            for file in self.files
        ]
        params["signers"] = [
            {
                "name": signer.name,
                "email": signer.email,
                "phone": signer.phone,
                "files": signer._files_to_list(),
                "type": signer.type,
                "access_code": signer.access_code,
                "force_signature_type": signer.force_signature_type,
            }
            for signer in self.signers
        ]
        return _crush(params) or {}

    def send_to_sign(self):
        body = self.extract_api_params()
        encoded = FormUrlEncoded(body).extract_to_str()
        return self.send_request("post", "signature", {"body": encoded})

    # Unsupported methods from Task
    def download(self, *args, **kwargs):
        raise UnsupportedFunctionalityError("Method not implemented")

    def delete(self):
        raise UnsupportedFunctionalityError("Method not implemented")

    def enable_file_encryption(self, *args, **kwargs):
        raise UnsupportedFunctionalityError("Method not implemented")

    def assign_meta_value(self, *args, **kwargs):
        raise UnsupportedFunctionalityError("Method not implemented")


def _crush(value: Any):
    if isinstance(value, dict):
        result = {k: _crush(v) for k, v in value.items()}
        result = {k: v for k, v in result.items() if v is not None}
        return result or None
    if isinstance(value, list):
        result = [_crush(v) for v in value]
        result = [v for v in result if v is not None]
        return result or None
    return value
