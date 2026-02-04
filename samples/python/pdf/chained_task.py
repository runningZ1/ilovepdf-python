from ilovepdf import Ilovepdf
from _config import PUBLIC_KEY, SECRET_KEY

ilovepdf = Ilovepdf(PUBLIC_KEY, SECRET_KEY)

compress_task = ilovepdf.new_task("compress")
compress_task.add_file("/path/to/file.pdf")
compress_task.execute()

# Chain to another task
merge_task = compress_task.next("merge")
merge_task.add_file("/path/to/another.pdf")
merge_task.execute()
merge_task.download()
