from ilovepdf.tool import Officepdf
from _config import PUBLIC_KEY, SECRET_KEY

office_task = Officepdf(PUBLIC_KEY, SECRET_KEY)
office_task.add_file("/path/to/document.docx")
office_task.execute()
office_task.download()
