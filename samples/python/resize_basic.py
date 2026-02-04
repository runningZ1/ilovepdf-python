from ilovepdf import Iloveimg
from _config import PUBLIC_KEY, SECRET_KEY

iloveimg = Iloveimg(PUBLIC_KEY, SECRET_KEY)

task = iloveimg.new_task("resize")

task.add_file("/path/to/file.jpg")

task.resize_mode = "pixels"
task.pixels_width = 500
task.pixels_height = 500

task.execute()
task.download()
