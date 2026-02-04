from ilovepdf import Iloveimg
from _config import PUBLIC_KEY, SECRET_KEY

iloveimg = Iloveimg(PUBLIC_KEY, SECRET_KEY)

task = iloveimg.new_task("crop")

task.add_file("/path/to/file.jpg")

task.x = 10
task.y = 10
task.width = 25
task.height = 50

task.execute()
task.download()
