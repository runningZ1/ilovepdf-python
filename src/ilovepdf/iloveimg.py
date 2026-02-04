from __future__ import annotations

from .ilovepdf import Ilovepdf


class Iloveimg(Ilovepdf):
    IMAGE_TOOL_ALIASES = {
        "compress": "compressimage",
        "rotate": "rotateimage",
        "watermark": "watermarkimage",
    }

    def new_task(self, tool_name: str, make_start: bool = True):
        tool_name_str = str(tool_name)
        mapped = self.IMAGE_TOOL_ALIASES.get(tool_name_str, tool_name_str)
        return super().new_task(mapped, make_start)
