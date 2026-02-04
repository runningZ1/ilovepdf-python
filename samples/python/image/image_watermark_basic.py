from ilovepdf import Iloveimg
from ilovepdf.element import Element
from _config import PUBLIC_KEY, SECRET_KEY

iloveimg = Iloveimg(PUBLIC_KEY, SECRET_KEY)

task = iloveimg.new_task("watermark")

task.add_file("/path/to/file.png")

element = Element({
    "type": "text",
    "text": "iLoveAPI",
    "gravity": "Center",
    "transparency": 50,
    "width_percent": 30,
    "height_percent": 10,
})
task.add_element(element)

task.execute()
task.download()
