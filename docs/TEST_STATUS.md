测试状态
========

最后更新：2026-02-04

图片工具（本地 API 烟测）
-------------------------

输入文件：
- `D:\Download\Gemini_Generated_Image_h9jit1h9jit1h9ji(1).png`
- `D:\Download\4152392682ab38fb1294bfc5a3c73da2.png`
- `D:\Download\1月8日-视频封面.png`

结果：
- 通过：`compress`、`resize`、`crop`、`convert`、`rotate`、`watermark`、`repair`、
  `upscale`、`removebackground`

说明：
- `repairimage` 可能受 API 计划限制，如果提示工具不存在，可使用 PDF 的 `repair`
  作为替代。

PDF 工具
--------

代码结构拆分为 `tool/pdf` 与 `tool/image` 之后，尚未重新回归测试。
之前的已知结果（拆分前）：
- 通过：`compress`、`merge`、`split`、`pdfa`、`validatepdfa`、`rotate`、`repair`、
  `protect`、`watermark`、`pagenumber`、`pdfjpg`、`extract`
- 跳过：`imagepdf`（需要图片输入）、`officepdf`（需要 Office 文档）、
  `unlock`（需要带密码的 PDF）
- 失败：`signature`（API 计划签名额度不足）
