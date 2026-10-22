#!/usr/bin/env bash
# Test runner for the YAML converter tests.
#
# Usage:
#   ./test.sh [--output_path <junit.xml>] <base|new>
#
#   base  run the existing repository tests; these must pass both before and
#         after the solution is applied.
#   new   run the new tests; these fail before the solution and pass after it.
set -uo pipefail

cd /app

OUTPUT_PATH=""
if [ "${1:-}" = "--output_path" ]; then
  OUTPUT_PATH="$2"
  shift 2
fi

MODE="${1:-new}"

TEST_LOG="$(mktemp)"
STATUS=0

run_tests() {
  regex="$1"
  shift
  if [ -n "$regex" ]; then
    python -m pytest "$@" -k "$regex" -v 2>&1 | tee -a "$TEST_LOG"
  else
    python -m pytest "$@" -v 2>&1 | tee -a "$TEST_LOG"
  fi
  status=${PIPESTATUS[0]}
  if [ "$status" -ne 0 ]; then
    STATUS=$status
  fi
}

case "$MODE" in
  base)
    if [ -n "$OUTPUT_PATH" ]; then
      python -m pytest packages/markitdown/tests/test_module_misc.py packages/markitdown/tests/test_html_converter.py -v --junitxml="$OUTPUT_PATH" -k "not test_markitdown_remote and not test_speech_transcription" 2>&1 | tee -a "$TEST_LOG"
      status=${PIPESTATUS[0]}
      if [ "$status" -ne 0 ]; then
        STATUS=$status
      fi
    else
      run_tests "" packages/markitdown/tests/test_module_misc.py packages/markitdown/tests/test_html_converter.py -k "not test_markitdown_remote and not test_speech_transcription"
    fi
    ;;
  new)
    if [ -n "$OUTPUT_PATH" ]; then
      python -m pytest packages/markitdown/tests/test_yaml_converter_328df3.py -v --junitxml="$OUTPUT_PATH" 2>&1 | tee -a "$TEST_LOG"
      status=${PIPESTATUS[0]}
      if [ "$status" -ne 0 ]; then
        STATUS=$status
      fi
    else
      run_tests "" packages/markitdown/tests/test_yaml_converter_328df3.py
    fi
    ;;
  *)
    echo "unknown mode: $MODE (expected base or new)" >&2
    exit 2
    ;;
esac

exit "$STATUS"
