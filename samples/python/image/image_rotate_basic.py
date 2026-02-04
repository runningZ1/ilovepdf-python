from ilovepdf import Iloveimg
from _config import PUBLIC_KEY, SECRET_KEY

iloveimg = Iloveimg(PUBLIC_KEY, SECRET_KEY)

task = iloveimg.new_task("rotate")

file1 = task.add_file("/path/to/file.jpg")
file1.rotate = 90

task.execute()
task.download()
