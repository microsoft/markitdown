#!/usr/bin/env bash
# Per-format regression smoke test for the built markitdown CLI + MCP server.
# Shared by app-ci.yml and app-release.yml so both gates are identical and the
# released binary is proven to handle every supported format on every OS/arch.
#
# Usage:  BIN=<dir-with-binaries> bash .github/scripts/smoke.sh <label>
# Run from the repository root (fixtures are under packages/...).
set -euo pipefail

label="${1:-local}"
: "${BIN:?set BIN to the directory containing the built binaries}"
# OS-aware executable suffix: GitHub sets RUNNER_OS; outside Actions, Windows
# (Git Bash / MSYS) sets OS=Windows_NT or reports MINGW*/MSYS* in `uname`.
EXE=""
case "${RUNNER_OS:-}${OS:-}$(uname -s 2>/dev/null || echo)" in
  *Windows* | *MINGW* | *MSYS* | *CYGWIN*) EXE=".exe" ;;
esac
CLI="$BIN/markitdown$EXE"
MCP="$BIN/markitdown-mcp$EXE"
FX="packages/markitdown/tests/test_files"

# All scratch output goes to a temp dir that is removed on exit, so the script
# never litters the repo (in CI or when a developer runs it locally).
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

echo "== smoke + format regression on: $label =="
"$CLI" --version
"$CLI" --list-formats > "$WORK/formats.txt"
grep -qi PDF "$WORK/formats.txt"

# One real fixture per format / optional-dependency group. Every one must
# convert to NON-EMPTY Markdown (exit 0). Images / audio / web pages are
# "degraded" without the Python engine but still emit metadata, so they are
# valid non-empty conversions here. A new change that breaks any converter, or
# silently drops one from the registry, fails this gate.
fixtures="\
test.pdf \
test.docx \
test.xlsx \
test.xls \
test.pptx \
test_outlook_msg.msg \
test_notebook.ipynb \
test_mskanji.csv \
test.epub \
test_blog.html \
test_rss.xml \
test.json \
test.jpg \
test.wav \
test.mp3 \
test.m4a"

checked=0
missing=0
for f in $fixtures; do
  if [[ ! -f "$FX/$f" ]]; then
    echo "::warning::fixture missing, skipped: $f"
    missing=$((missing + 1))
    continue
  fi
  "$CLI" "$FX/$f" > "$WORK/conv_out.md"
  if [[ ! -s "$WORK/conv_out.md" ]]; then
    echo "::error::empty conversion output for $f"
    exit 1
  fi
  echo "  ok  $f  ($(wc -c < "$WORK/conv_out.md" | tr -d ' ') bytes)"
  checked=$((checked + 1))
done
echo "converted $checked fixtures ($missing missing)"

# Negative regression: a non-document must be rejected with a non-zero exit.
if "$CLI" "$FX/random.bin" > /dev/null 2>&1; then
  echo "::error::random.bin was accepted but must be rejected"
  exit 1
fi
echo "  ok  random.bin correctly rejected"

# MCP server: a real stdio JSON-RPC handshake must advertise the convert tool.
printf '%s\n%s\n%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"ci","version":"0"}}}' \
  '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
  > "$WORK/mcp_req.txt"
"$MCP" < "$WORK/mcp_req.txt" > "$WORK/mcp_resp.txt"
grep -q convert_to_markdown "$WORK/mcp_resp.txt"
echo "  ok  mcp tools/list handshake"

echo "== regression PASS on: $label =="
