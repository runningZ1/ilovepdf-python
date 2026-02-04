from __future__ import annotations

from ilovepdf.errors import Error
from ilovepdf.helper import camelize_str, underscore_str
from ilovepdf.ilovepdf import Ilovepdf


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
        from . import tool as tool_module

        tool_name_str = str(tool_name)
        normalized = tool_name_str.replace("-", "_").lower()
        mapped = self.IMAGE_TOOL_ALIASES.get(normalized, tool_name_str)

        camelized_name = camelize_str(mapped)
        task_class = getattr(tool_module, camelized_name, None)
        if not task_class:
            normalized = mapped.replace("-", "_")
            for class_name, klass in tool_module.TOOL_CLASSES.items():
                if underscore_str(class_name) == normalized:
                    task_class = klass
                    break
        if not task_class:
            raise Error(
                f"Unknown tool '{mapped}'. Available tools: {self.all_tool_names()}"
            )
        return task_class(self._public_key, self._secret_key, make_start)

    @classmethod
    def all_tool_names(cls):
        from . import tool as tool_module

        return [underscore_str(name) for name in tool_module.TOOL_CLASSES.keys()]
