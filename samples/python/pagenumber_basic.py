from ilovepdf.tool import Pagenumber
from _config import PUBLIC_KEY, SECRET_KEY

pagenumber_task = Pagenumber(PUBLIC_KEY, SECRET_KEY)
pagenumber_task.add_file("/path/to/file.pdf")
pagenumber_task.pages = "1-end"
pagenumber_task.starting_number = 1
pagenumber_task.font_size = 12
pagenumber_task.text = "{n}"

pagenumber_task.execute()
pagenumber_task.download()
