from .pdf.compress import Compress
from .pdf.extract import Extract
from .pdf.imagepdf import Imagepdf
from .pdf.htmlpdf import Htmlpdf
from .pdf.merge import Merge
from .pdf.officepdf import Officepdf
from .pdf.pagenumber import Pagenumber
from .pdf.pdfa import Pdfa
from .pdf.pdfjpg import Pdfjpg
from .pdf.pdfocr import Pdfocr
from .pdf.protect import Protect
from .pdf.repair import Repair
from .pdf.rotate import Rotate
from .pdf.split import Split
from .pdf.unlock import Unlock
from .pdf.validate_pdfa import ValidatePdfa
from .pdf.watermark import Watermark

TOOL_CLASSES = {
    "Compress": Compress,
    "Extract": Extract,
    "Imagepdf": Imagepdf,
    "Htmlpdf": Htmlpdf,
    "Merge": Merge,
    "Officepdf": Officepdf,
    "Pagenumber": Pagenumber,
    "Pdfa": Pdfa,
    "Pdfjpg": Pdfjpg,
    "Pdfocr": Pdfocr,
    "Protect": Protect,
    "Repair": Repair,
    "Rotate": Rotate,
    "Split": Split,
    "Unlock": Unlock,
    "ValidatePdfa": ValidatePdfa,
    "Watermark": Watermark,
}

__all__ = list(TOOL_CLASSES.keys())
