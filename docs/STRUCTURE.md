项目结构
========

本仓库将 PDF 与图片功能分开，使用者可以通过目录与文件名快速定位工具与示例。

源代码
------

- `src/ilovepdf/tool/pdf`: PDF 工具实现
  - `compress.py`、`merge.py`、`split.py`、`repair.py`、`watermark.py` 等
- `src/ilovepdf/tool/image`: 图片工具实现
  - `resize.py`、`crop.py`、`convert.py`、`compressimage.py`、`upscaleimage.py` 等

公开客户端
----------

- `src/ilovepdf/ilovepdf.py`: PDF API 客户端
- `src/ilovepdf/iloveimg.py`: 图片 API 客户端（将易用的工具名映射到 `*image`）

示例
----

- `samples/python/pdf`: PDF 处理示例
- `samples/python/image`: 图片处理示例
- `samples/python/signature`: 签名 API 示例

测试
----

- `tests`: 轻量单元测试（请求编码与客户端映射）
