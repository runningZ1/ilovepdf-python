功能总览
========

本仓库提供 iLovePDF（PDF）与 iLoveAPI（图片）两类能力，分别由不同客户端使用：

- PDF 客户端：`Ilovepdf`
- 图片客户端：`Iloveimg`

PDF 功能
--------

工具名与用途：

- `compress`：压缩 PDF
- `merge`：合并多个 PDF
- `split`：拆分 PDF
- `officepdf`：Office 文档转 PDF
- `pdfjpg`：PDF 转 JPG
- `imagepdf`：图片转 PDF
- `pagenumber`：添加页码
- `rotate`：旋转 PDF
- `unlock`：解锁 PDF
- `protect`：加密 PDF
- `watermark`：添加水印（文本或图片）
- `repair`：修复 PDF
- `pdfa`：PDF 转 PDF/A
- `validatepdfa`：验证 PDF/A
- `extract`：提取（如页面、内容等）
- `signature`：电子签名流程

图片功能
--------

工具名与用途：

- `resize`：图片缩放
- `crop`：图片裁剪
- `compress`：图片压缩
- `convert`：图片格式转换
- `rotate`：图片旋转
- `watermark`：图片水印（基于 `elements`）
- `repair`：图片修复（部分账户可能不可用）
- `upscale`：图片放大
- `removebackground`：图片去背景

注意：图片工具通过 `Iloveimg` 使用，内部会映射到 API 的 `*image` 工具名，
例如 `compress` -> `compressimage`，`removebackground` -> `removebackgroundimage`。

示例位置
--------

- `samples/python/pdf`：PDF 处理示例
- `samples/python/image`：图片处理示例
- `samples/python/signature`：签名相关示例
