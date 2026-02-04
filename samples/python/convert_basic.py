from ilovepdf import Iloveimg
from _config import PUBLIC_KEY, SECRET_KEY

iloveimg = Iloveimg(PUBLIC_KEY, SECRET_KEY)

task = iloveimg.new_task("convert")

task.add_file("/path/to/file.jpg")

task.to = "gif"
task.gif_time = 50
task.gif_loop = True

task.execute()
task.download()
