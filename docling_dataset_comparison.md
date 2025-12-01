# Docling vs MarkItDown on Docling Test Dataset

This report compares Docling ground truth outputs (docling_v2) with the current MarkItDown conversion on the PDF and TIFF files from the [docling test data](https://github.com/docling-project/docling/tree/main/tests/data) dataset. For each document we compute the normalized similarity ratio between Docling and MarkItDown Markdown outputs, and the absolute/normalized differences between first line bounding box coordinates.

| File | Markdown similarity | Markdown diff (%) | x1 abs | y1 abs | x2 abs | y2 abs | x1 norm | y1 norm | x2 norm | y2 norm | Avg bbox diff (%) |
|------|--------------------:|------------------:|-------:|-------:|-------:|-------:|--------:|--------:|--------:|--------:|------------------:|
| 2203.01017v2 | 0.68 | 32.00 | 0.00 | 1.44 | 0.00 | 0.00 | 0.0000 | 0.0018 | 0.0000 | 0.0000 | 0.04 |
| 2206.01062 | 0.55 | 45.00 | 0.00 | 1.77 | 0.00 | 0.18 | 0.0000 | 0.0022 | 0.0000 | 0.0002 | 0.06 |
| 2305.03393v1-pg9 | 0.78 | 22.00 | 0.00 | 0.16 | 33.04 | 0.74 | 0.0000 | 0.0002 | 0.0540 | 0.0009 | 1.38 |
| 2305.03393v1 | 0.77 | 23.00 | 0.00 | 1.67 | 0.00 | 0.00 | 0.0000 | 0.0021 | 0.0000 | 0.0000 | 0.05 |
| amt_handbook_sample | 0.48 | 52.00 | 44.91 | 658.38 | 438.61 | 656.85 | 0.0756 | 0.8506 | 0.7384 | 0.8486 | 62.83 |
| code_and_formula | 0.67 | 33.00 | 0.00 | 1.72 | 0.00 | 0.03 | 0.0000 | 0.0022 | 0.0000 | 0.0000 | 0.06 |
| multi_page | 0.97 | 3.00 | 0.00 | 1.47 | 0.00 | 0.66 | 0.0000 | 0.0017 | 0.0000 | 0.0008 | 0.06 |
| picture_classification | 0.98 | 2.00 | 0.00 | 1.72 | 0.01 | 0.03 | 0.0000 | 0.0022 | 0.0000 | 0.0000 | 0.06 |
| redp5110_sampled | 0.53 | 47.00 | 250.92 | 724.48 | 320.24 | 714.36 | 0.4100 | 0.9148 | 0.5233 | 0.9020 | 68.75 |
| right_to_left_01 | 0.05 | 95.00 | 63.72 | 1.45 | 0.00 | 0.70 | 0.1041 | 0.0018 | 0.0000 | 0.0009 | 2.67 |
| right_to_left_02 | 0.02 | 98.00 | 23.15 | 594.43 | 378.81 | 595.51 | 0.0389 | 0.7060 | 0.6364 | 0.7073 | 52.22 |
| right_to_left_03 | 0.08 | 92.00 | 419.00 | 48.07 | 238.12 | 51.77 | 0.7038 | 0.0571 | 0.4000 | 0.0615 | 30.56 |
| 2206.01062_tif | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| **Overall (avg)** | 0.55 | 45.33 |  |  |  |  |  |  |  |  | 18.23 |

Overall, MarkItDown's Markdown output is about **54.7%** similar to the Docling ground truth (45.33% different) across the 12 supported documents. Bounding box coordinates diverge by an average of **18.23%**, with right-to-left samples and scanned forms contributing most of the error.
