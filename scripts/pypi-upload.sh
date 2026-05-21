#!/bin/bash
# 上传 markitdown-glmocr 和 markitdown-paddleocr 到 PyPI
# 用法: ./scripts/pypi-upload.sh [version]
#   version: 可选，指定版本号，默认上传 dist 目录下所有文件

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== PyPI Upload Script ===${NC}"
echo ""

# 从 Windows 用户环境变量读取 PYPI_API_TOKEN
if [ -z "$PYPI_API_TOKEN" ]; then
    PYPI_API_TOKEN=$(powershell -Command "[System.Environment]::GetEnvironmentVariable('PYPI_API_TOKEN', 'User')" 2>/dev/null)
fi

if [ -z "$PYPI_API_TOKEN" ] || [ "$PYPI_API_TOKEN" = "(no output)" ]; then
    echo -e "${RED}错误: 未找到 PYPI_API_TOKEN 环境变量${NC}"
    echo "请设置 PYPI_API_TOKEN 环境变量或在 Windows 用户环境变量中配置"
    exit 1
fi

echo -e "${GREEN}✓ PyPI API Token 已加载${NC}"
echo ""

# 设置 UTF-8 编码避免 Windows GBK 问题
export PYTHONUTF8=1

VERSION="${1:-}"
PACKAGES=("markitdown-glmocr" "markitdown-paddleocr")

for PKG in "${PACKAGES[@]}"; do
    PKG_DIR="$PROJECT_ROOT/packages/$PKG"
    
    if [ ! -d "$PKG_DIR/dist" ]; then
        echo -e "${YELLOW}跳过 $PKG: dist 目录不存在${NC}"
        continue
    fi
    
    echo -e "${GREEN}--- 上传 $PKG ---${NC}"
    
    # 获取包名格式 (markitdown-glmocr -> markitdown_glmocr)
    PKG_NAME=$(echo "$PKG" | tr '-' '_')
    
    # 确定要上传的文件
    if [ -n "$VERSION" ]; then
        UPLOAD_FILES="$PKG_DIR/dist/${PKG_NAME}-${VERSION}*"
    else
        UPLOAD_FILES="$PKG_DIR/dist/${PKG_NAME}*"
    fi
    
    # 检查文件是否存在
    if ls $UPLOAD_FILES 1> /dev/null 2>&1; then
        echo "文件:"
        ls $UPLOAD_FILES
        echo ""
        
        twine upload --username __token__ --password "$PYPI_API_TOKEN" --disable-progress-bar $UPLOAD_FILES
        
        # 从输出中提取版本号
        LATEST_VERSION=$(ls $UPLOAD_FILES | head -1 | grep -oP '\d+\.\d+\.\d+' | head -1)
        echo -e "${GREEN}✓ $PKG 上传成功!${NC}"
        echo "  https://pypi.org/project/$PKG/${LATEST_VERSION:-latest}/"
        echo ""
    else
        echo -e "${YELLOW}跳过 $PKG: 未找到版本 ${VERSION:-任何} 的构建文件${NC}"
        echo ""
    fi
done

echo -e "${GREEN}=== 上传完成 ===${NC}"
