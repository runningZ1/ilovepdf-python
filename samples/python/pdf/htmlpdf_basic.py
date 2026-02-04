from ilovepdf import Ilovepdf
from _config import PUBLIC_KEY, SECRET_KEY

ilovepdf = Ilovepdf(PUBLIC_KEY, SECRET_KEY)

task = ilovepdf.new_task("htmlpdf")

task.page_size = "A4"
task.page_orientation = "portrait"
task.page_margin = 10

task.add_file_from_url("https://example.com")

task.execute()
task.download()
