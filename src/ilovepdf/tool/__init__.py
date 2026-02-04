from .compress import Compress
from .compressimage import Compressimage
from .convert import Convert
from .crop import Crop
from .extract import Extract
from .imagepdf import Imagepdf
from .merge import Merge
from .officepdf import Officepdf
from .pagenumber import Pagenumber
from .pdfa import Pdfa
from .pdfjpg import Pdfjpg
from .protect import Protect
from .repair import Repair
from .resize import Resize
from .rotate import Rotate
from .rotateimage import Rotateimage
from .signature import Signature
from .split import Split
from .unlock import Unlock
from .validate_pdfa import ValidatePdfa
from .watermark import Watermark
from .watermarkimage import Watermarkimage

TOOL_CLASSES = {
    "Compress": Compress,
    "Compressimage": Compressimage,
    "Convert": Convert,
    "Crop": Crop,
    "Extract": Extract,
    "Imagepdf": Imagepdf,
    "Merge": Merge,
    "Officepdf": Officepdf,
    "Pagenumber": Pagenumber,
    "Pdfa": Pdfa,
    "Pdfjpg": Pdfjpg,
    "Protect": Protect,
    "Repair": Repair,
    "Resize": Resize,
    "Rotate": Rotate,
    "Rotateimage": Rotateimage,
    "Signature": Signature,
    "Split": Split,
    "Unlock": Unlock,
    "ValidatePdfa": ValidatePdfa,
    "Watermark": Watermark,
    "Watermarkimage": Watermarkimage,
}

__all__ = list(TOOL_CLASSES.keys())
