from __future__ import annotations

from .file import File


class SignatureFile(File):
    def __init__(self, server_filename: str, filename: str) -> None:
        super().__init__(server_filename, filename)
        self.recipients = []
