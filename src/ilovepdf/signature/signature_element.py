from __future__ import annotations

from .file_element import FileElement


class SignatureElement(FileElement):
    def __init__(self, file):
        super().__init__(file)
        self.type = "signature"
