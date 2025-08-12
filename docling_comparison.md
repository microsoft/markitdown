# Docling vs MarkItDown on ocr_test.pdf

This document compares the outputs of [Docling](https://github.com/docling-project/docling) and the current MarkItDown implementation on the sample `ocr_test.pdf`.

## Markdown comparison
- Normalized similarity ratio: 1.00

```diff
--- docling
+++ markitdown
@@ -1 +1,3 @@
-Docling bundles PDF document conversion to JSON and Markdown in an easy self contained package
+Docling bundles PDF document conversion to
+JSON and Markdown in an easy self contained
+package
```

## Bounding box comparison (first line)
Page size (MarkItDown): 1654 x 2339 px

| coordinate | Docling (scaled) | MarkItDown | abs diff | norm diff |
|-----------:|------------------:|-----------:|---------:|----------:|
| x1 | 193.63 | 205.00 | 11.37 | 0.0069 |
| y1 | 213.92 | 217.00 | 3.08 | 0.0013 |
| x2 | 1402.98 | 1398.00 | 4.98 | 0.0030 |
| y2 | 424.81 | 268.00 | 156.81 | 0.0670 |

