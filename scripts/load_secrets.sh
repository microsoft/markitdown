#!/bin/bash
# 加载本地敏感配置

if [ -f ".secrets.local" ]; then
    echo "Loading secrets from .secrets.local"
    set -a
    source .secrets.local
    set +a
    echo "✓ Secrets loaded"
else
    echo "✗ .secrets.local not found"
    exit 1
fi
