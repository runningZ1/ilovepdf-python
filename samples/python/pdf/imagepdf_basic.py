from ilovepdf.tool import Imagepdf
from _config import PUBLIC_KEY, SECRET_KEY

imagepdf_task = Imagepdf(PUBLIC_KEY, SECRET_KEY)
imagepdf_task.orientation = "portrait"
imagepdf_task.pagesize = "A4"
imagepdf_task.add_file("/path/to/image1.jpg")
imagepdf_task.add_file("/path/to/image2.png")
imagepdf_task.execute()
imagepdf_task.download()
