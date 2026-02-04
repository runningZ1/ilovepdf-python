from ilovepdf.tool import Pdfjpg
from _config import PUBLIC_KEY, SECRET_KEY

pdfjpg_task = Pdfjpg(PUBLIC_KEY, SECRET_KEY)
pdfjpg_task.add_url("https://example.com")
pdfjpg_task.execute()
pdfjpg_task.download()
