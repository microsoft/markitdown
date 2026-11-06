# Measured synthetic baseline

Converter commit: `7482c092d9c0074a89803c9fdb63a969e7fe17fc`. Python 3.13.5; macOS-26.7.1-x86_64-i386-64bit-Mach-O.

4 acceptance passes, 18 confirmed acceptance failures. These historical failures are retained for comparison; the current implementation passes all 22 acceptance cases (see current.json).

| Category | Cases | Pass | Mean CER | Mean WER | Mean order accuracy |
|---|---:|---:|---:|---:|---:|
| basic | 2 | 0 | 0.8324 | 1.0000 | N/A |
| layout | 3 | 0 | 0.7924 | 1.0000 | 0.0 |
| mixed | 4 | 0 | 1.2483 | 1.5893 | N/A |
| unicode | 3 | 0 | 0.7287 | 1.0000 | N/A |
| numeric | 3 | 3 | 0.0000 | 0.0000 | N/A |
| embedded | 4 | 0 | 1.9167 | 2.0327 | N/A |
| table | 1 | 0 | 0.7179 | 0.7059 | 0.027777777777777776 |
| control | 2 | 1 | 0.1739 | 0.2500 | 0.8333333333333334 |

| Fixture | Acceptance | CER | WER | Classification |
|---|---|---:|---:|---|
| basic_sentence | FAIL | 0.8077 | 1.0000 | Character reversal |
| sentences | FAIL | 0.8571 | 1.0000 | Character reversal |
| paragraphs | FAIL | 0.7647 | 1.0000 | Character reversal |
| heading | FAIL | 0.8125 | 1.0000 | Character reversal |
| python_version | FAIL | 0.6000 | 0.8571 | Bidirectional corruption |
| file_identifier | FAIL | 0.5714 | 1.0000 | Bidirectional corruption |
| model_identifier | FAIL | 0.8421 | 1.0000 | Bidirectional corruption |
| contract_date | FAIL | 2.9796 | 3.5000 | Layout corruption |
| letter_variants | FAIL | 0.5714 | 1.0000 | Character reversal |
| zwnj | FAIL | 0.8148 | 1.0000 | Character reversal |
| persian_digits | PASS | 0.0000 | 0.0000 | — |
| arabic_digits | PASS | 0.0000 | 0.0000 | — |
| ascii_digits | PASS | 0.0000 | 0.0000 | — |
| diacritics | FAIL | 0.8000 | 1.0000 | Character reversal |
| url | FAIL | 2.9444 | 3.7143 | Layout corruption |
| email | FAIL | 0.3704 | 0.6667 | Bidirectional corruption |
| decimal_unit | FAIL | 0.8333 | 1.0000 | Bidirectional corruption |
| parentheses_math | FAIL | 3.5185 | 2.7500 | Layout corruption |
| rtl_table | FAIL | 0.7179 | 0.7059 | Table corruption |
| two_column_rtl | FAIL | 0.8000 | 1.0000 | Layout corruption |
| ltr_sentence | PASS | 0.0000 | 0.0000 | — |
| two_column_ltr | FAIL | 0.3478 | 0.5000 | Layout corruption |

Table structure accuracy: 0.0; correct shape: true. Matching dimensions alone did not preserve cell associations. See baseline.json for exact expected/actual strings, Unicode diagnostics and both underlying-library outputs.

Validation: 60 local PDF/support tests passed and 18 xfailed; the existing remote PDF test passed separately with network access. Full repository and multi-platform CI were not run. Regeneration preserved all PDF SHA-256 hashes.

This is a synthetic baseline, not a claim about failure frequency in naturally occurring documents. Human sign-off and real-world coverage remain open (README.md).
