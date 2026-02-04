from ilovepdf.element import Element
from ilovepdf.tool import Watermark
from _config import PUBLIC_KEY, SECRET_KEY

watermark_task = Watermark(PUBLIC_KEY, SECRET_KEY)
watermark_task.add_file("/path/to/file.pdf")

watermark = Element({
    "type": "text",
    "text": "CONFIDENTIAL",
    "pages": "all",
    "font_size": 36,
    "transparency": 50,
})
watermark_task.add_element(watermark)

watermark_task.execute()
watermark_task.download()
