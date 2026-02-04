from ilovepdf import Iloveimg
from _config import PUBLIC_KEY, SECRET_KEY

iloveimg = Iloveimg(PUBLIC_KEY, SECRET_KEY)

task = iloveimg.new_task("compress")

task.add_file("/path/to/file.jpg")

task.execute()
task.download()
