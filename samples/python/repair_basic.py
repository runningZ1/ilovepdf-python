from ilovepdf.tool import Repair
from _config import PUBLIC_KEY, SECRET_KEY

repair_task = Repair(PUBLIC_KEY, SECRET_KEY)
repair_task.add_file("/path/to/file.pdf")
repair_task.execute()
repair_task.download()
