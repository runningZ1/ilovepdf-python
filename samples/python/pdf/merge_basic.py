from ilovepdf.tool import Merge
from _config import PUBLIC_KEY, SECRET_KEY

merge_task = Merge(PUBLIC_KEY, SECRET_KEY)
merge_task.add_file("/path/to/file1.pdf")
merge_task.add_file("/path/to/file2.pdf")
merge_task.execute()
merge_task.download()
