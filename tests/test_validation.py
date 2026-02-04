import pytest

from ilovepdf.element import Element
from ilovepdf.errors import ArgumentEnumError
from ilovepdf.file import File


def test_element_rejects_invalid_font_family():
    with pytest.raises(ArgumentEnumError):
        Element({"font_family": "NotAFont"})


def test_file_rotate_validation():
    file = File("server", "name.pdf")
    with pytest.raises(ArgumentEnumError):
        file.rotate = 45
