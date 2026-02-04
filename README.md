iLovePDF API - Python 库
-----------------------
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

iLovePDF API 的 Python SDK，包含 iLoveAPI 的图片处理工具。

可用于开发并自动化以下 PDF 处理任务：

- 压缩 PDF
- 合并 PDF
- 拆分 PDF
- Office 转 PDF
- PDF 转 JPG
- 图片转 PDF
- 添加页码
- 旋转 PDF
- 解锁 PDF
- 加密 PDF
- 添加水印
- 修复 PDF
- PDF 转 PDF/A
- 校验 PDF/A
- 提取
- PDF 签名

每个功能都有对应的参数设置以获得期望结果。

同样支持图片处理功能，例如：

- 图片缩放
- 图片裁剪
- 图片压缩
- 图片格式转换
- 图片旋转
- 图片水印
- 图片修复
- 图片放大
- 图片去背景

## 环境要求
Python 3.8 或更高版本

## 安装

```bash
pip install ilovepdf-python
```

## 使用方法

### 快速开始
最快的方式是先获取 API Key，然后运行下面的代码示例：

```python
from ilovepdf import Ilovepdf

public_key = "YOUR_PUBLIC_KEY"
private_key = "YOUR_PRIVATE_KEY"

ilovepdf = Ilovepdf(public_key, private_key)

# 创建一个任务并指定所需工具：
task = ilovepdf.new_task("compress")

# 添加需要上传的文件...
file1 = task.add_file("my_disk/my_example1.pdf")
file2 = task.add_file("my_disk/my_example2.pdf")
file3 = task.add_file_from_url("http://URL_TO_PDF")

# 上传完成后执行任务：
task.execute()
task.download()
```

更多示例请参考本仓库的 sample 目录。

### 文档

- `docs/STRUCTURE.md`: 项目结构（PDF 与图片分离）
- `docs/TEST_STATUS.md`: 最新测试状态
- `docs/FEATURES.md`: 功能总览（全部工具列表）

### 示例结构

- `samples/python/pdf`: PDF 处理示例
- `samples/python/image`: 图片处理示例
- `samples/python/signature`: 签名 API 示例

### 源码结构

- `src/ilovepdf/tool/pdf`: PDF 工具实现
- `src/ilovepdf/tool/image`: 图片工具实现

## 签名工具
该工具的使用方式与其他工具不同，下面示例展示如何创建签名请求：

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

更多签名相关示例请参考仓库内的 sample 代码。

## API 文档

### HTTP API 调用
所有 PDF 与图片工具都支持以下方法与 iLovePDF API 交互：

| 方法                   | 说明                                                     | 备注                                            |
| ---------------------- | -------------------------------------------------------- | ----------------------------------------------- |
| add_file(file)         | 上传文件到 iLovePDF 服务器                               | 返回 File                                       |
| add_file_from_url(url) | 通过 URL 上传文件到 iLovePDF 服务器                      | 返回 File                                       |
| delete_file(file)      | 删除 iLovePDF 服务器上的文件                             | 返回 boolean                                    |
| download(path)         | 下载处理后的文件                                         | 返回 boolean；无需指定完整文件路径              |
| status()               | 获取当前任务的处理状态                                   | 返回 Response                                   |
| execute()              | 发送处理请求开始任务                                     | 返回 Response                                   |
| delete()               | 删除任务                                                 | 返回 Response                                   |

示例：
```python
from ilovepdf.tool import Imagepdf

imagepdf_task = Imagepdf(public_key, secret_key)
http_response = imagepdf_task.execute()
print(http_response.body)
if imagepdf_task.download():
    print("文件下载成功！")
```

### 所有工具通用方法

| 方法                                 | 说明                                                                                         | 备注                                         |
| ------------------------------------ | -------------------------------------------------------------------------------------------- | -------------------------------------------- |
| enable_file_encryption(enable, key)  | 处理前使用该 key 解密文件，处理后再加密回去                                                  | 若不提供 key，会自动生成随机 key             |
| assign_meta_value(key, value)        | 为输出文件设置元数据                                                                        |                                              |
| ignore_errors                        | 设为 true 时，处理时忽略错误                                                                 | 默认：true                                   |
| ignore_password                      | 设为 true 时，忽略带密码文件                                                                 | 默认：true                                   |
| try_pdf_repair                       | 设为 true 时，处理失败会尝试修复 PDF                                                         | 默认：true                                   |
| packaged_filename                    | 多文件下载时设置压缩包文件名                                                                 |                                              |
| output_filename                      | 设置最终输出文件名                                                                          |                                              |

### 工具属性
每个工具都有对应的可配置属性。例如图片转 PDF 工具：

```python
from ilovepdf.tool import Imagepdf

print(Imagepdf.API_PARAMS)
# -> ["orientation", "margin", "pagesize", "merge_after"]
```

直接实例化 Compress 工具示例：

```python
from ilovepdf.tool import Compress

compress_task = Compress(public_key, secret_key)
```

### 图片工具
图片工具通过 `Iloveimg` 客户端暴露，内部会将易用的工具名映射到正确的 API 工具名
（例如 `compress` -> `compressimage`，`removebackground` -> `removebackgroundimage`）。

注意：部分图片工具（例如 `repairimage`）可能取决于你的 API 套餐权限。
如果 API 提示工具不存在，可尝试使用 PDF 的 `repair` 作为替代。

图片缩放示例：

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

图片水印示例：

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

### 错误处理

当某个接口出现 API 错误时，可以用下面方式捕获：

```python
from ilovepdf import ApiError
from ilovepdf.tool import Compress

try:
    compress_task = Compress(public_key, secret_key)
    compress_task.execute()  # 若未上传文件会抛出错误
    compress_task.download()
except ApiError as exc:
    print(exc.http_response.body)
```

更多最新文档请参考 https://developer.ilovepdf.com/docs 。

## 许可证

本库基于 MIT License 开源。
