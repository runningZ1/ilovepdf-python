from ilovepdf.tool import Unlock
from _config import PUBLIC_KEY, SECRET_KEY

unlock_task = Unlock(PUBLIC_KEY, SECRET_KEY)
file = unlock_task.add_file("/path/to/locked.pdf")
file.password = "your_password"
unlock_task.execute()
unlock_task.download()
