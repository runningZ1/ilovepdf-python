iLovePDF API - Python SDK
-------------------------
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python SDK for the iLovePDF API, including iLoveIMG image tools.

Highlights:
- Python SDK + CLI, so you can automate tasks or run one-off commands quickly
- CLI is convenient for scripts and integrates cleanly with ClaudeSkill
- Based on https://github.com/ilovepdf/ilovepdf-ruby with structural refactors
- Full parameter coverage to match the official API tools

You can use this SDK to automate PDF tasks such as:

- Compress PDF
- Merge PDF
- Split PDF
- Office to PDF
- HTML to PDF
- PDF to JPG
- OCR PDF
- Image to PDF
- Add page numbers
- Rotate PDF
- Unlock PDF
- Protect PDF
- Add watermark
- Repair PDF
- PDF to PDF/A
- Validate PDF/A
- Extract pages

It also supports image processing tools, for example:

- Resize
- Crop
- Compress
- Convert format
- Rotate
- Watermark
- Upscale
- Remove background

Each tool exposes parameters so you can fine-tune the output.

## Requirements
Python 3.8+.

## Installation

```bash
pip install ilovepdf-python
```

## Usage

### Quick start
Get your API keys, then run the following example:

```python
from ilovepdf import Ilovepdf

public_key = "YOUR_PUBLIC_KEY"
secret_key = "YOUR_PRIVATE_KEY"

ilovepdf = Ilovepdf(public_key, secret_key)

# Create a task and select a tool:
task = ilovepdf.new_task("compress")

# Add files...
file1 = task.add_file("my_disk/my_example1.pdf")
file2 = task.add_file("my_disk/my_example2.pdf")
file3 = task.add_file_from_url("http://URL_TO_PDF")

# Execute and download:
task.execute()
task.download()
```

More examples are included in the snippets below (the repo no longer ships extra example files).

## CLI
After installation, you can run `ilovepdf` / `iloveimg`:

```bash
# PDF compress
ilovepdf pdf compress --file ./input.pdf --output-dir ./out

# Image resize
ilovepdf img resize --file ./input.png --param resize_mode=pixels --param pixels_width=800 --param pixels_height=600 --output-dir ./out

# Load keys from a .env file
ilovepdf pdf merge --file a.pdf --file b.pdf --env-file ./.env --output-dir ./out
```

Available options:
- `--public-key` / `--secret-key`: API keys
- `--env-file`: Load environment variables (`ILOVEPDF_PUBLIC_KEY` / `ILOVEPDF_SECRET_KEY`)
- `--param key=value`: Tool parameter (repeatable)
- `--params-json path.json`: Load all parameters from a JSON file
- `--no-download`: Process only, do not download
- `--timeout` / `--long-timeout`: Timeout (seconds)
- `--json`: Output JSON result

## Project structure

- `src/ilovepdf`: PDF module (shared base logic)
- `src/ilovepdf/tool/pdf`: PDF tool implementations
- `src/iloveimg`: Image module
- `src/iloveimg/tool`: Image tool implementations

## API

### HTTP API usage
All PDF and image tools share these API interaction methods:

| Method                | Description                                   | Notes                                      |
| --------------------- | --------------------------------------------- | ------------------------------------------ |
| add_file(file)        | Upload a file to iLovePDF servers             | Returns File                               |
| add_file_from_url(url)| Upload a file by URL                          | Returns File                               |
| delete_file(file)     | Delete a file from iLovePDF servers           | Returns boolean                            |
| download(path)        | Download processed file                       | Returns boolean; no full path is required  |
| status()              | Get current task status                       | Returns Response                           |
| execute()             | Start the task                                | Returns Response                           |
| delete()              | Delete the task                               | Returns Response                           |

Example:
```python
from ilovepdf.tool import Imagepdf

imagepdf_task = Imagepdf(public_key, secret_key)
http_response = imagepdf_task.execute()
print(http_response.body)
if imagepdf_task.download():
    print("Download complete")
```

### Common methods for all tools

| Method                                 | Description                                                     | Notes                                |
| -------------------------------------- | --------------------------------------------------------------- | ------------------------------------ |
| enable_file_encryption(enable, key)    | Decrypt before processing and re-encrypt after                 | If key is empty, a random key is generated |
| assign_meta_value(key, value)          | Set output file metadata                                        |                                      |
| ignore_errors                          | Ignore errors during processing                                 | Default: true                        |
| ignore_password                        | Ignore password-protected files                                 | Default: true                        |
| try_pdf_repair                         | Attempt PDF repair on failure                                   | Default: true                        |
| packaged_filename                      | Set output ZIP filename for multi-file downloads                |                                      |
| output_filename                        | Set the final output filename                                   |                                      |

### Tool attributes
Each tool exposes configurable attributes. For example, Image to PDF:

```python
from ilovepdf.tool import Imagepdf

print(Imagepdf.API_PARAMS)
# -> ["orientation", "margin", "pagesize", "merge_after"]
```

Instantiate a specific tool directly:

```python
from ilovepdf.tool import Compress

compress_task = Compress(public_key, secret_key)
```

### Image tools
Image tools are exposed via the `Iloveimg` client, which maps friendly names to the official API names
(e.g., `compress` -> `compressimage`, `removebackground` -> `removebackgroundimage`).

If the API reports a missing tool, you can try the PDF `repair` tool as a fallback.

Resize example:

```python
from iloveimg import Iloveimg

iloveimg = Iloveimg(public_key, secret_key)
task = iloveimg.new_task("resize")

task.add_file("path/to/file.jpg")
task.resize_mode = "pixels"
task.pixels_width = 500
task.pixels_height = 500

task.execute()
task.download()
```

Watermark example:

```python
from iloveimg import Iloveimg
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

### Error handling

When the API returns an error, catch it as follows:

```python
from ilovepdf import ApiError
from ilovepdf.tool import Compress

try:
    compress_task = Compress(public_key, secret_key)
    compress_task.execute()  # Raises if no files were added
    compress_task.download()
except ApiError as exc:
    print(exc.http_response.body)
```

For the latest API docs, see https://developer.ilovepdf.com/docs.

## License

MIT License.
