from ilovepdf.tool import ValidatePdfa
from _config import PUBLIC_KEY, SECRET_KEY

validate_task = ValidatePdfa(PUBLIC_KEY, SECRET_KEY)
validate_task.conformance = "pdfa-2b"
validate_task.add_file("/path/to/file.pdf")
response = validate_task.execute()
print(response.body)
