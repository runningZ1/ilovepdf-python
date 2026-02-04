Test Status
===========

Last updated: 2026-02-04

Image Tools (local API smoke test)
----------------------------------

Inputs:
- `D:\Download\Gemini_Generated_Image_h9jit1h9jit1h9ji(1).png`
- `D:\Download\4152392682ab38fb1294bfc5a3c73da2.png`
- `D:\Download\1月8日-视频封面.png`

Results:
- PASS: `compress`, `resize`, `crop`, `convert`, `rotate`, `watermark`, `repair`,
  `upscale`, `removebackground`

Notes:
- `repairimage` can be restricted by API plan. If your plan does not allow it,
  use the PDF `repair` tool as fallback.

PDF Tools
---------

Not re-tested after the codebase was reorganized into `tool/pdf` and `tool/image`.
Previously known results (before the reorg):
- PASS: `compress`, `merge`, `split`, `pdfa`, `validatepdfa`, `rotate`, `repair`,
  `protect`, `watermark`, `pagenumber`, `pdfjpg`, `extract`
- SKIP: `imagepdf` (needs images), `officepdf` (needs Office file),
  `unlock` (needs password-protected PDF)
- FAIL: `signature` (insufficient signature credits on API plan)
