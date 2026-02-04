iLovePDF Api - Python Library
---------------------------
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python SDK for the iLovePDF API, including image tools from iLoveAPI.

Develop and automate PDF processing tasks like:

- Compress PDF
- Merge PDF
- Split PDF
- Convert Office to PDF
- PDF to JPG
- Images to PDF
- Add Page Numbers
- Rotate PDF
- Unlock PDF
- Protect PDF
- Stamp a Watermark
- Repair PDF
- PDF to PDF/A
- Validate PDF/A
- Extract
- Sign PDF

Each one with several settings to get your desired results.

You can also process images with tools like:

- Resize images
- Crop images
- Compress images
- Convert images
- Rotate images
- Watermark images
- Repair images
- Upscale images
- Remove image backgrounds

## Requirements
Python 3.8 or greater

## Installation

```bash
pip install ilovepdf-python
```

## Usage

### Getting started
The quickest way to get started is to first get a set of API keys and run the following code snippet:

```python
from ilovepdf import Ilovepdf

public_key = "YOUR_PUBLIC_KEY"
private_key = "YOUR_PRIVATE_KEY"

ilovepdf = Ilovepdf(public_key, private_key)

# Create a task with the tool you want to use:
task = ilovepdf.new_task("compress")

# Add the files you want to upload...
file1 = task.add_file("my_disk/my_example1.pdf")
file2 = task.add_file("my_disk/my_example2.pdf")
file3 = task.add_file_from_url("http://URL_TO_PDF")

# Once you are done uploading your files:
task.execute()
task.download()
```

For a more in-depth usage, refer to the sample codes in this repository.

### Samples layout

- `samples/python/pdf`: PDF processing examples
- `samples/python/image`: Image processing examples
- `samples/python/signature`: Signature API examples

### Source layout

- `src/ilovepdf/tool/pdf`: PDF tool implementations
- `src/ilovepdf/tool/image`: Image tool implementations

## Signature Tool
The usage of this tool is different than the other tools. The following example shows how to create a signature using the iLovePDF API:

```python
from ilovepdf.tool import Signature
from ilovepdf.signature import Receiver, SignatureElement

my_task = Signature(pub_key, priv_key)
file = my_task.add_file("/path/to/file/sample.pdf")

signer = Receiver("signer", "name", "email@email.com")

signature_element = SignatureElement(file)
signature_element.set_position(x=20, y=-20)
signature_element.pages = "1"
signature_element.size = 40

signer.add_element(signature_element)
my_task.add_receiver(signer)
response = my_task.send_to_sign()
body = response.body
```

For a more in-depth usage, refer to all of the signature examples on the sample codes in this repository.

## Documentation

### HTTP API Calls
All PDF and image tools have the following methods that contact the iLovePDF API:

| Method                 | Description                                              | Notes                                           |
| ---------------------- | -------------------------------------------------------- | ----------------------------------------------- |
| add_file(file)         | Uploads a file to iLovePDF servers                       | Returns File                                    |
| add_file_from_url(url) | Uploads a file to iLovePDF servers using a URL           | Returns File                                    |
| delete_file(file)      | Deletes a file from iLovePDF                             | Returns boolean                                 |
| download(path)         | Downloads the processed file                             | Returns boolean; no need to specify a filepath  |
| status()               | Retrieves the current status of the task being processed | Returns Response                                |
| execute()              | Sends a request to iLovePDF to begin processing the PDFs | Returns Response                                |
| delete()               | Deletes the task                                         | Returns Response                                |

Example:
```python
from ilovepdf.tool import Imagepdf

imagepdf_task = Imagepdf(public_key, secret_key)
http_response = imagepdf_task.execute()
print(http_response.body)
if imagepdf_task.download():
    print("Your file was downloaded successfully!")
```

### Methods common to all tools

| Method                               | Description                                                                                 | Notes                                        |
| ------------------------------------ | ------------------------------------------------------------------------------------------- | -------------------------------------------- |
| enable_file_encryption(enable, key)  | The key will be used to decrypt the files before processing and re-encrypt them after      | If no key provided, a random key is assigned |
| assign_meta_value(key, value)        | Assigns metadata values for output files                                                    |                                              |
| ignore_errors                        | If true, ignores errors on processing                                                       | Default: true                                |
| ignore_password                      | If true, ignores password-protected files                                                   | Default: true                                |
| try_pdf_repair                       | If true, try to repair a PDF when processing fails                                          | Default: true                                |
| packaged_filename                    | Specify filename of the compressed file when multiple files are downloaded                  |                                              |
| output_filename                      | Set the final name of the processed file                                                    |                                              |

### Tool attributes
All tools have specific attributes you can access and modify. For example for the Image to PDF tool:

```python
from ilovepdf.tool import Imagepdf

print(Imagepdf.API_PARAMS)
# -> ["orientation", "margin", "pagesize", "merge_after"]
```

To instantiate a Compress tool task directly do:

```python
from ilovepdf.tool import Compress

compress_task = Compress(public_key, secret_key)
```

### Image tools
Image tools are exposed through the `Iloveimg` client, which maps image tool names
to the correct API tools (for example `compress` -> `compressimage`,
`removebackground` -> `removebackgroundimage`).

Note: Some image tools (such as `repairimage`) may depend on your API plan. If the
API reports the tool does not exist, try the PDF `repair` tool as a fallback.

Example usage for image resize:

```python
from ilovepdf import Iloveimg

iloveimg = Iloveimg(public_key, secret_key)
task = iloveimg.new_task("resize")

task.add_file("path/to/file.jpg")
task.resize_mode = "pixels"
task.pixels_width = 500
task.pixels_height = 500

task.execute()
task.download()
```

Image watermark example:

```python
from ilovepdf import Iloveimg
from ilovepdf.element import Element

iloveimg = Iloveimg(public_key, secret_key)
task = iloveimg.new_task("watermark")

task.add_file("path/to/file.png")

element = Element({
    "type": "text",
    "text": "iLoveAPI",
    "gravity": "Center",
    "transparency": 50,
    "width_percent": 30,
    "height_percent": 10,
})
task.add_element(element)

task.execute()
task.download()
```

### Handling errors

Whenever there is an API Error in one of the endpoints, you can try to capture it the following way:

```python
from ilovepdf import ApiError
from ilovepdf.tool import Compress

try:
    compress_task = Compress(public_key, secret_key)
    compress_task.execute()  # This raises an error if you forgot to upload a file
    compress_task.download()
except ApiError as exc:
    print(exc.http_response.body)
```

Please see https://developer.ilovepdf.com/docs for up-to-date documentation.

## License

The library is available as open source under the terms of the MIT License.
