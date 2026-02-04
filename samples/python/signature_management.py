from ilovepdf.signature import Management
from _config import PUBLIC_KEY, SECRET_KEY

management = Management(PUBLIC_KEY, SECRET_KEY)

# List signatures
response = management.list_signatures()
print(response.body)

# Download signed document (replace TOKEN)
# management.download_signed("SIGNATURE_TOKEN", directory=".", filename="signed")
