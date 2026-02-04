from ilovepdf import Ilovepdf
from _config import PUBLIC_KEY, SECRET_KEY

ilovepdf = Ilovepdf(PUBLIC_KEY, SECRET_KEY)

task = ilovepdf.new_task("pdfocr")

task.add_file("/path/to/file.pdf")

task.execute()
task.download()
