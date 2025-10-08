#!/bin/bash
# Helper script to build the markitdown-mcp Docker image
# This script ensures fresh builds that pick up code changes

set -e

cd "$(dirname "$0")/../.."

echo "Building markitdown-mcp Docker image..."
echo "Timestamp: $(date +%s)"

# Build with cache-busting argument to force rebuild of Python packages
docker build \
  -f packages/markitdown-mcp/Dockerfile \
  --build-arg CACHE_BUST=$(date +%s) \
  -t markitdown-mcp:latest \
  .

echo ""
echo "✅ Build complete!"
echo ""
echo "To restart the service with the new image:"
echo "  cd packages/markitdown-mcp"
echo "  docker compose down"
echo "  docker compose up -d"
