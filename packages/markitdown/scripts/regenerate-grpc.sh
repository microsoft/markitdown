#!/usr/bin/env bash
# Regenerates the checked-in gRPC stubs from proto/markitdown/v1/markitdown.proto.
#
# Usage:
#   pip install "grpcio-tools>=1.81.0"
#   ./scripts/regenerate-grpc.sh
#
# The proto package is `markitdown.v1`, but the generated Python modules live
# inside the `markitdown.grpc.v1` package so they ship with the library. The
# import rewrite below accounts for that difference.
set -euo pipefail

cd "$(dirname "$0")/.."

OUT_DIR="src/markitdown/grpc"

python3 -m grpc_tools.protoc \
  --proto_path=proto \
  --python_out="${OUT_DIR}" \
  --grpc_python_out="${OUT_DIR}" \
  proto/markitdown/v1/markitdown.proto

# protoc emits to <out>/markitdown/v1; relocate into the grpc/v1 package.
mv "${OUT_DIR}/markitdown/v1/markitdown_pb2.py" "${OUT_DIR}/v1/markitdown_pb2.py"
mv "${OUT_DIR}/markitdown/v1/markitdown_pb2_grpc.py" "${OUT_DIR}/v1/markitdown_pb2_grpc.py"
rm -rf "${OUT_DIR}/markitdown"

# Rewrite the absolute import to match the package layout.
sed -i.bak \
  's/^from markitdown\.v1 import markitdown_pb2/from markitdown.grpc.v1 import markitdown_pb2/' \
  "${OUT_DIR}/v1/markitdown_pb2_grpc.py"
rm -f "${OUT_DIR}/v1/markitdown_pb2_grpc.py.bak"

# Keep formatting consistent with the repo's pre-commit hooks.
if command -v black >/dev/null 2>&1; then
  black -q "${OUT_DIR}/v1/markitdown_pb2.py" "${OUT_DIR}/v1/markitdown_pb2_grpc.py"
fi

echo "Regenerated gRPC stubs in ${OUT_DIR}/v1/"
