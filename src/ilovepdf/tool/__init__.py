from .pdf.compress import Compress
from .image.compressimage import Compressimage
from .image.convert import Convert
from .image.crop import Crop
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
from .image.resize import Resize
from .pdf.rotate import Rotate
from .image.rotateimage import Rotateimage
from .image.upscaleimage import Upscaleimage
from .image.removebackgroundimage import Removebackgroundimage
from .pdf.split import Split
from .pdf.unlock import Unlock
from .pdf.validate_pdfa import ValidatePdfa
from .pdf.watermark import Watermark
from .image.watermarkimage import Watermarkimage

TOOL_CLASSES = {
    "Compress": Compress,
    "Compressimage": Compressimage,
    "Convert": Convert,
    "Crop": Crop,
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
    "Resize": Resize,
    "Rotate": Rotate,
    "Rotateimage": Rotateimage,
    "Upscaleimage": Upscaleimage,
    "Removebackgroundimage": Removebackgroundimage,
    "Split": Split,
    "Unlock": Unlock,
    "ValidatePdfa": ValidatePdfa,
    "Watermark": Watermark,
    "Watermarkimage": Watermarkimage,
}

__all__ = list(TOOL_CLASSES.keys())
