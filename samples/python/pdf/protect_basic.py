from ilovepdf.tool import Protect
from _config import PUBLIC_KEY, SECRET_KEY

protect_task = Protect(PUBLIC_KEY, SECRET_KEY)
protect_task.password = "secret"
protect_task.add_file("/path/to/file.pdf")
protect_task.execute()
protect_task.download()
