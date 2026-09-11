"""Download a public Google Sheet as XLSX and render it to Markdown."""
import argparse
import io
import os
import sys

import requests

# Make sibling module importable when invoked as `python scripts/sync_sheet.py`.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_xlsx import render_workbook  # noqa: E402


def fetch_xlsx(sheet_id: str) -> bytes:
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
    # Browser-ish UA avoids occasional 403s from Google's export endpoint.
    resp = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0 (sync-from-google-sheets)"},
        allow_redirects=True,
        timeout=60,
    )
    resp.raise_for_status()
    return resp.content


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--sheet-id", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()

    xlsx_bytes = fetch_xlsx(args.sheet_id)
    markdown = render_workbook(io.BytesIO(xlsx_bytes))
    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(markdown)
    print(f"Wrote {args.output} ({len(markdown)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
