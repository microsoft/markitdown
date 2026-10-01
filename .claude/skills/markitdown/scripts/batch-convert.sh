#!/bin/bash
# Batch convert documents to Markdown using MarkItDown CLI
#
# Usage:
#   ./batch-convert.sh ./documents ./output
#   ./batch-convert.sh ./documents ./output pdf,docx,pptx
#   ./batch-convert.sh ./documents ./output pdf 4  # 4 parallel jobs

set -euo pipefail

INPUT_DIR="${1:?Usage: $0 <input_dir> <output_dir> [extensions] [parallel_jobs]}"
OUTPUT_DIR="${2:?Usage: $0 <input_dir> <output_dir> [extensions] [parallel_jobs]}"
EXTENSIONS="${3:-}"
PARALLEL_JOBS="${4:-4}"

# Check if markitdown is installed
if ! command -v markitdown &>/dev/null; then
    echo "Error: markitdown not installed. Run: pip install 'markitdown[all]'"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Build find command based on extensions
if [[ -n "$EXTENSIONS" ]]; then
    # Convert comma-separated extensions to find arguments
    IFS=',' read -ra EXT_ARRAY <<< "$EXTENSIONS"
    FIND_ARGS=()
    for i in "${!EXT_ARRAY[@]}"; do
        ext="${EXT_ARRAY[$i]}"
        ext="${ext#.}"  # Remove leading dot if present
        if [[ $i -eq 0 ]]; then
            FIND_ARGS+=("-name" "*.$ext")
        else
            FIND_ARGS+=("-o" "-name" "*.$ext")
        fi
    done
    FILES=$(find "$INPUT_DIR" -maxdepth 1 -type f \( "${FIND_ARGS[@]}" \))
else
    FILES=$(find "$INPUT_DIR" -maxdepth 1 -type f)
fi

# Count files
FILE_COUNT=$(echo "$FILES" | grep -c . || echo 0)

if [[ "$FILE_COUNT" -eq 0 ]]; then
    echo "No files found in $INPUT_DIR"
    exit 0
fi

echo "Input: $INPUT_DIR"
echo "Output: $OUTPUT_DIR"
[[ -n "$EXTENSIONS" ]] && echo "Extensions: $EXTENSIONS"
echo "Files: $FILE_COUNT"
echo "Parallel jobs: $PARALLEL_JOBS"
echo ""

# Convert function for parallel execution
convert_file() {
    local input_file="$1"
    local output_dir="$2"
    local filename
    filename=$(basename "$input_file")
    local name="${filename%.*}"
    local output_file="$output_dir/$name.md"

    if markitdown "$input_file" -o "$output_file" 2>/dev/null; then
        echo "OK: $filename"
    else
        echo "FAIL: $filename" >&2
    fi
}

export -f convert_file
export OUTPUT_DIR

# Check if GNU parallel is available
if command -v parallel &>/dev/null; then
    echo "$FILES" | parallel -j "$PARALLEL_JOBS" convert_file {} "$OUTPUT_DIR"
else
    # Fallback to xargs
    echo "$FILES" | xargs -P "$PARALLEL_JOBS" -I {} bash -c 'convert_file "$@"' _ {} "$OUTPUT_DIR"
fi

echo ""
echo "Conversion complete. Output in: $OUTPUT_DIR"
