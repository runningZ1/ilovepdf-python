from ilovepdf.tool import Pdfa
from _config import PUBLIC_KEY, SECRET_KEY

pdfa_task = Pdfa(PUBLIC_KEY, SECRET_KEY)
pdfa_task.conformance = "pdfa-2b"
pdfa_task.add_file("/path/to/file.pdf")
pdfa_task.execute()
pdfa_task.download()
