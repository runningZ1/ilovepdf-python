from __future__ import annotations

import os
from urllib.parse import unquote

from ..task import Task


class Management(Task):
    def __init__(self, public_key: str, secret_key: str, make_start: bool = False) -> None:
        self.tool = "sign"
        super().__init__(public_key, secret_key, make_start)

    def get_status(self, signature_token: str):
        return self.send_request("get", f"signature/requesterview/{signature_token}")

    def list_signatures(self, current_page: int = 0, per_page: int = 20):
        return self.send_request("get", "signature/list", {"body": {"page": current_page, "per_page": per_page}})

    def download_audit(self, signature_token: str, directory: str | None = None, create_directory: bool = True, filename: str | None = None):
        return self._download_file(f"signature/{signature_token}/download-audit", directory, create_directory, filename)

    def download_original(self, signature_token: str, directory: str | None = None, create_directory: bool = True, filename: str | None = None):
        return self._download_file(f"signature/{signature_token}/download-original", directory, create_directory, filename)

    def download_signed(self, signature_token: str, directory: str | None = None, create_directory: bool = True, filename: str | None = None):
        return self._download_file(f"signature/{signature_token}/download-signed", directory, create_directory, filename)

    def send_reminders(self, signature_token: str):
        return self.send_request("post", f"signature/sendReminder/{signature_token}")

    def void_signature(self, signature_token: str):
        return self.send_request("put", f"signature/void/{signature_token}")

    def increase_expiration_days(self, signature_token: str, days_to_increase: int):
        body = {"days": days_to_increase}
        return self.send_request("put", f"signature/increase-expiration-days/{signature_token}", {"body": body})

    def get_receiver_info(self, signer_token: str):
        return self.send_request("get", f"signature/receiver/info/{signer_token}")

    def fix_receiver_email(self, signer_token: str, new_email: str):
        body = {"email": new_email}
        return self.send_request("put", f"signature/receiver/fix-email/{signer_token}", {"body": body})

    def fix_receiver_phone(self, signer_token: str, new_phone: str):
        body = {"phone": new_phone}
        return self.send_request("put", f"signature/receiver/fix-phone/{signer_token}", {"body": body})

    def _download_file(self, url: str, directory: str | None, create_directory: bool, filename: str | None):
        if self.worker_server is None:
            response = self.perform_start_request()
            self.worker_server = f"https://{response.body['server']}"

        response = self.send_request("get", url)
        content_disposition = response.headers.get("content-disposition")
        external_filename = self._parse_filename_from_content_disposition(content_disposition)
        filename_to_set = os.path.splitext(filename)[0] if filename else None

        if filename_to_set is None:
            filename_to_set = external_filename
        else:
            filename_to_set = f"{filename_to_set}{os.path.splitext(external_filename or '')[1]}"

        if directory:
            directory = os.fspath(directory)
            if directory.endswith("/"):
                directory = directory[:-1]
        else:
            directory = "."

        destination = os.path.join(directory, filename_to_set)
        if create_directory:
            os.makedirs(directory, exist_ok=True)
        with open(destination, "wb") as file_handle:
            file_handle.write(response.raw_body)
        return destination

    def _parse_filename_from_content_disposition(self, content_disposition: str | None):
        if not content_disposition:
            return None
        if "filename*=" in content_disposition:
            parts = content_disposition.split("filename*=")
            if len(parts) > 1:
                value = parts[1]
                if "''" in value:
                    value = value.split("''", 1)[1]
                return unquote(value.replace('"', ""))
        if "filename=" in content_disposition:
            value = content_disposition.split("filename=")[-1]
            return value.replace('"', "").strip()
        return None
