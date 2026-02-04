from __future__ import annotations

from typing import Any, Dict, Generator, Iterable, Optional

from .errors import ArgumentEnumError
from .pdf_page import PdfPage


class File:
    ROTATION_VALUES = [0, 90, 180, 270]

    def __init__(self, server_filename: str, filename: str) -> None:
        self.server_filename = server_filename
        self.filename = filename
        self.password: Optional[str] = None
        self.info: Optional[dict] = None
        self.pdf_pages: Optional[Iterable[str]] = None
        self.pdf_forms: Optional[Iterable[dict]] = None
        self.pdf_page_number: Optional[int] = None
        self._rotate: Optional[int] = None
        self._deleted = False

    @property
    def rotate(self) -> Optional[int]:
        return self._rotate

    @rotate.setter
    def rotate(self, degrees: int) -> None:
        if degrees not in self.ROTATION_VALUES:
            raise ArgumentEnumError(self.ROTATION_VALUES)
        self._rotate = degrees

    def file_options(self) -> Dict[str, Any]:
        payload = {
            "server_filename": self.server_filename,
            "filename": self.filename,
            "rotate": self.rotate,
        }
        if self.password:
            payload["password"] = self.password
        return payload

    def pdf_page_info(self, page_number: int) -> Optional[PdfPage]:
        if not self.pdf_pages:
            return None
        if page_number <= 0:
            return None
        try:
            pdf_page_string = list(self.pdf_pages)[page_number - 1]
        except IndexError:
            return None
        if not isinstance(pdf_page_string, str):
            return None
        return PdfPage.from_string(pdf_page_string)

    def last_pdf_page(self) -> Optional[Iterable[str]]:
        return self.pdf_pages

    def each_pdf_form_element(self) -> Generator:
        if not self.pdf_forms:
            return
        for pdf_form_element in self.pdf_forms:
            pdf_page = self.pdf_page_info(pdf_form_element.get("page"))
            yield pdf_form_element, pdf_page

    def mark_as_deleted(self) -> None:
        self._deleted = True

    def deleted(self) -> bool:
        return self._deleted
