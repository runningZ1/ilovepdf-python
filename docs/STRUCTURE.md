Project Structure
=================

This repository separates PDF and Image functionality so users can locate tools
and examples quickly by folder and filename.

Source Code
-----------

- `src/ilovepdf/tool/pdf`: PDF tool implementations
  - `compress.py`, `merge.py`, `split.py`, `repair.py`, `watermark.py`, ...
- `src/ilovepdf/tool/image`: Image tool implementations
  - `resize.py`, `crop.py`, `convert.py`, `compressimage.py`, `upscaleimage.py`, ...

Public Clients
--------------

- `src/ilovepdf/ilovepdf.py`: PDF API client
- `src/ilovepdf/iloveimg.py`: Image API client (maps friendly tool names to `*image`)

Samples
-------

- `samples/python/pdf`: PDF processing examples
- `samples/python/image`: Image processing examples
- `samples/python/signature`: Signature API examples

Tests
-----

- `tests`: Lightweight unit tests for request encoding and client mappings
