from .compressimage import Compressimage
from .convert import Convert
from .crop import Crop
from .removebackgroundimage import Removebackgroundimage
from .resize import Resize
from .rotateimage import Rotateimage
from .upscaleimage import Upscaleimage
from .watermarkimage import Watermarkimage

TOOL_CLASSES = {
    "Compressimage": Compressimage,
    "Convert": Convert,
    "Crop": Crop,
    "Resize": Resize,
    "Rotateimage": Rotateimage,
    "Upscaleimage": Upscaleimage,
    "Removebackgroundimage": Removebackgroundimage,
    "Watermarkimage": Watermarkimage,
}

__all__ = list(TOOL_CLASSES.keys())
