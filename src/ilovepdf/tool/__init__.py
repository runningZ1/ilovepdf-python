from .compress import Compress
from .extract import Extract
from .imagepdf import Imagepdf
from .merge import Merge
from .officepdf import Officepdf
from .pagenumber import Pagenumber
from .pdfa import Pdfa
from .pdfjpg import Pdfjpg
from .protect import Protect
from .repair import Repair
from .rotate import Rotate
from .signature import Signature
from .split import Split
from .unlock import Unlock
from .validate_pdfa import ValidatePdfa
from .watermark import Watermark

TOOL_CLASSES = {
    "Compress": Compress,
    "Extract": Extract,
    "Imagepdf": Imagepdf,
    "Merge": Merge,
    "Officepdf": Officepdf,
    "Pagenumber": Pagenumber,
    "Pdfa": Pdfa,
    "Pdfjpg": Pdfjpg,
    "Protect": Protect,
    "Repair": Repair,
    "Rotate": Rotate,
    "Signature": Signature,
    "Split": Split,
    "Unlock": Unlock,
    "ValidatePdfa": ValidatePdfa,
    "Watermark": Watermark,
}

__all__ = list(TOOL_CLASSES.keys())
