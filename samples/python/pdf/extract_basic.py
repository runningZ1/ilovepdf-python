from ilovepdf.tool import Extract
from _config import PUBLIC_KEY, SECRET_KEY

extract_task = Extract(PUBLIC_KEY, SECRET_KEY)
extract_task.detailed = True
extract_task.add_file("/path/to/file.pdf")
response = extract_task.execute()
print(response.body)
