#!/bin/bash
set -e
IN="$1"
[ -f "$IN" ] || { echo "File not found: $IN" >&2; exit 1; }
python3 -c "import markitdown" 2>/dev/null || pip install -q "markitdown[pdf,pptx,docx,xlsx,xls]" >&2
OUTDIR="${MD_OUTDIR:-/mnt/user-data/outputs}"
mkdir -p "$OUTDIR" 2>/dev/null || OUTDIR="$(dirname "$IN")"
OUT="$OUTDIR/$(basename "${IN%.*}").md"
python3 -m markitdown "$IN" -o "$OUT"
echo "$OUT"
echo "$(wc -l < "$OUT") lines, $(wc -c < "$OUT") bytes"
