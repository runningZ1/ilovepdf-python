from ilovepdf import ApiError
from ilovepdf.tool import Compress
from _config import PUBLIC_KEY, SECRET_KEY

try:
    compress_task = Compress(PUBLIC_KEY, SECRET_KEY)
    compress_task.execute()  # This raises if you forgot to upload files
    compress_task.download()
except ApiError as exc:
    print(exc.http_response.body)
