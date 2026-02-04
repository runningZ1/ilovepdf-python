from ilovepdf import Iloveimg
from _config import PUBLIC_KEY, SECRET_KEY

iloveimg = Iloveimg(PUBLIC_KEY, SECRET_KEY)

task = iloveimg.new_task("upscale")

task.add_file("/path/to/file.jpg")
task.multiplier = 2

task.execute()
task.download()
