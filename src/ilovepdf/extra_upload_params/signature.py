from __future__ import annotations

from .base import Base


class Signature(Base):
    def set_pdf_info(self, activate: bool = True) -> "Signature":
        self.set_value("pdfinfo", "1" if bool(activate) else "0")
        return self

    def set_pdf_forms(self, activate: bool = True) -> "Signature":
        is_active = bool(activate)
        self.set_value("pdfforms", "1" if is_active else "0")
        if is_active:
            self.set_pdf_info(True)
        return self
