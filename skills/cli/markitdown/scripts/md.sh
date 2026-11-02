#!/bin/bash
# Convert a file to markdown locally (zero LLM tokens). Prints only the output path + stats.
set -e
DIR="$(cd "$(dirname "$0")/.." && pwd)"
IN="$1"
[ -f "$IN" ] || { echo "File not found: $IN" >&2; exit 1; }
OUTDIR="${MD_OUTDIR:-$(dirname "$IN")}"
OUT="$OUTDIR/$(basename "${IN%.*}").md"
"$DIR/.venv/bin/markitdown" "$IN" -o "$OUT"
echo "$OUT"
echo "$(wc -l < "$OUT") lines, $(wc -c < "$OUT") bytes (~$(( $(wc -c < "$OUT") / 4 )) tokens if fully read)"
