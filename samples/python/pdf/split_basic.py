from ilovepdf.tool import Split
from _config import PUBLIC_KEY, SECRET_KEY

split_task = Split(PUBLIC_KEY, SECRET_KEY)
split_task.add_file("/path/to/file.pdf")

# Split by ranges
split_task.ranges = "1-3,5"

split_task.execute()
split_task.download()
