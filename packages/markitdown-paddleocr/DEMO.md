# MarkItDown PaddleOCR Demo Notes

This document captures a minimal demo package for discussing
`markitdown-paddleocr` with maintainers or reviewers.

## Goal

Show a narrow but concrete gap:

- current MarkItDown returns empty output for scanned Chinese pages
- a local PaddleOCR backend can recover meaningful text
- this supports a plugin-first, opt-in, PDF-only first release

## Demo Setup

Environment used in this workspace:

- Python 3.13.5
- PaddlePaddle 3.3.1
- PaddleOCR 3.4.0
- MarkItDown installed from local editable source

OCR settings used for the first pass:

```python
{
    "use_doc_orientation_classify": False,
    "use_doc_unwarping": False,
    "use_textline_orientation": False,
}
```

These settings intentionally keep the demo simple and CPU-oriented.

## Samples

The demo was run against a small local set of redacted Chinese samples.
The sample files themselves are not required for the package, but the observed
categories were:

| Sample | Type | Characteristics |
| --- | --- | --- |
| `ocr_test_report.png` | report page | Chinese report text + chart labels + image caption + page number |
| `ocr_test_table.png` | table page | Chinese financial table with dense numeric cells |
| `ocr_test_math.jpg` | textbook page | Chinese educational page with formulas and diagrams |
| `orc_test_write.png` | notes page | handwritten / annotated style educational content |

For baseline PDF behavior, each image was also wrapped into a single-page PDF locally and run through the built-in MarkItDown PDF path.

## Before: current MarkItDown baseline

Two baseline checks were run:

1. direct image conversion via `MarkItDown()`
2. scanned-PDF conversion via `MarkItDown()` on image-wrapped PDFs

Observed result:

| Sample | Image baseline length | Wrapped PDF baseline length |
| --- | --- | --- |
| `ocr_test_math` | 0 | 0 |
| `ocr_test_report` | 0 | 0 |
| `ocr_test_table` | 0 | 0 |
| `orc_test_write` | 0 | 0 |

Interpretation:

- current built-in image conversion does not extract OCR text without an LLM path
- current built-in PDF conversion does not recover text from these scanned pages

This is the key "before" story.

## After: PaddleOCR extraction excerpts

### `ocr_test_report.png`

- Extracted text length: `806`
- What it successfully captured:
  - page title
  - chart axis values
  - year labels
  - Chinese paragraphs
  - English proper nouns like `KITUMBA` and `SINOMIN`
  - image caption
  - page number

Excerpt:

```text
中矿资源集团股份有限公司2024年年度报告全文
45,000
3,172
40,000
35,000
30,000
...
■自有矿实现锂盐销量
■外采矿实现锂盐销量
代加工实现锂盐销量
近年来公司锂电新能源板块销售情况（吨）
（三）地勘优势助力矿权开发，多金属布局取得新进展
近年来，公司主动调整固体矿产勘查业务方向，一方面对自有矿山提供技术支持...
KITUMBA
SINOMIN
Kitumba铜矿山开工典礼
...
31
```

### `ocr_test_table.png`

- Extracted text length: `1016`
- What it successfully captured:
  - financial table headers
  - row labels
  - dense numeric cells
  - paragraph notes below the table
  - page index

Excerpt:

```text
贵州茅台酒股份有限公司2025年半年度报告
4、营业收入和营业成本
（1）.营业收入和营业成本情况
√适用□不适用
单位：元币种：人民币
项目
本期发生额
上期发生额
收入
成本
收入
成本
主营业务
49,649,247,450.65
7,719,137,458.00
...
合计
49,679,827,345.61
7,763,157,196.73
...
101/103
```

### `ocr_test_math.jpg`

- Extracted text length: `937`
- What it successfully captured:
  - textbook heading and structure
  - most Chinese explanatory text
  - many symbols and variables
- Known limitation:
  - mathematical notation is partially noisy, which is expected for a first OCR-only pass

Excerpt:

```text
专题四曲线运动
241
C是第一级台阶水平面的中点。弹射器沿水平
...
答案 C
四、斜抛运动
1.分析思路：对斜上抛运动，从抛出点到最高
...
题型7
圆周运动中的临界极值问题
```

### `orc_test_write.png`

- Extracted text length: `436`
- What it successfully captured:
  - large handwritten / annotated title-like text
  - many labels from the diagram-heavy notes page
- Known limitation:
  - formula-like scribbles and diagram labels are noisier than report/table pages

Excerpt:

```text
知识系统化 作图习惯化答题规范化 积累常规化
②等效电队.
...
大招结论：
等效电路在哪边哪边匝数在分母上
...
学习自觉化 求知欲望化 高分习惯化
扫描全能王创建
```

## How to describe the result in an issue or PR

Recommended framing:

- current MarkItDown is strong for machine-readable PDFs
- the existing official OCR path is LLM-oriented
- scanned Chinese pages still have an offline OCR gap
- PaddleOCR demonstrates that a local CPU-friendly backend can recover useful text on report/table pages
- this should remain plugin-first and opt-in

Avoid framing it as:

- "add a Baidu feature to core"
- "replace the official OCR plugin"
- "solve OCR for every format in one PR"

## What this demo proves

It proves a realistic first-step story:

1. there is a measurable baseline gap
2. the gap is visible on Chinese report/table pages
3. a local OCR backend can materially improve extraction
4. this is suitable for a small plugin-first contribution path

## What this demo does not prove yet

- end-to-end PDF fallback timing for a production-sized document
- table structure reconstruction into rich Markdown tables
- mathematical OCR fidelity
- whether any upstream generic hook is needed

Those should be follow-up work, not part of the first maintainer conversation.
