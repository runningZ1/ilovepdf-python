from ilovepdf import Iloveimg
from _config import PUBLIC_KEY, SECRET_KEY

iloveimg = Iloveimg(PUBLIC_KEY, SECRET_KEY)

# Some accounts may not have this tool enabled. If you get a "tool does not exist"
# error, try `iloveimg.new_task("repair")` instead.
task = iloveimg.new_task("repairimage")

task.add_file("/path/to/file.jpg")

task.execute()
task.download()
