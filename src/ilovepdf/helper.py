import re


def underscore_str(value: str) -> str:
    if not value:
        return ""
    words = re.findall(r"[A-Z][a-z]*", value)
    if not words:
        return value.lower()
    return "_".join(word.lower() for word in words)


def camelize_str(value: str) -> str:
    if not value:
        return ""
    return "".join(part.capitalize() for part in value.split("_"))
