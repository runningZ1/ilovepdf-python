from ilovepdf.tool import Compress
from _config import PUBLIC_KEY, SECRET_KEY

compress_task = Compress(PUBLIC_KEY, SECRET_KEY)
compress_task.compression_level = "extreme"
compress_task.add_file("/path/to/file1.pdf")
compress_task.add_file("/path/to/file2.pdf")
compress_task.execute()
compress_task.download()
