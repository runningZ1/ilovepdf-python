from ilovepdf.tool import Rotate
from _config import PUBLIC_KEY, SECRET_KEY

rotate_task = Rotate(PUBLIC_KEY, SECRET_KEY)
file = rotate_task.add_file("/path/to/file.pdf")
file.rotate = 90
rotate_task.execute()
rotate_task.download()
