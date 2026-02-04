from __future__ import annotations

from .ilovepdf import Ilovepdf


class Iloveimg(Ilovepdf):
    IMAGE_TOOL_ALIASES = {
        "compress": "compressimage",
        "rotate": "rotateimage",
        "watermark": "watermarkimage",
        "upscale": "upscaleimage",
        "backgroundremove": "removebackgroundimage",
        "background_remove": "removebackgroundimage",
        "removebackground": "removebackgroundimage",
        "remove_background": "removebackgroundimage",
    }

    def new_task(self, tool_name: str, make_start: bool = True):
        tool_name_str = str(tool_name)
        normalized = tool_name_str.replace("-", "_").lower()
        mapped = self.IMAGE_TOOL_ALIASES.get(normalized, tool_name_str)
        return super().new_task(mapped, make_start)
