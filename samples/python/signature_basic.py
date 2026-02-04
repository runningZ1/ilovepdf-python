from ilovepdf.tool import Signature
from ilovepdf.signature import Receiver, SignatureElement
from _config import PUBLIC_KEY, SECRET_KEY

signature_task = Signature(PUBLIC_KEY, SECRET_KEY)
file = signature_task.add_file("/path/to/file.pdf")

signer = Receiver("signer", "Name", "email@example.com")

signature_element = SignatureElement(file)
signature_element.set_position(x=20, y=-20)
signature_element.pages = "1"
signature_element.size = 40

signer.add_element(signature_element)
signature_task.add_receiver(signer)

response = signature_task.send_to_sign()
print(response.body)
