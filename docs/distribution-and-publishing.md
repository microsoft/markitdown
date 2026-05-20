# MarkItDown 分发与发布方案

## 背景

本地 fork 版本包含两个核心包：
- **markitdown** `0.1.6b2`（官方 PyPI 最新为 `0.1.5`）
- **markitdown-glmocr** `0.1.0`（PyPI 上不存在，纯本地新增插件）

目标：让其他人能方便使用包含 glmocr 插件的 markitdown，不依赖官方是否合并 PR。

---

## 方案总览

| 方案 | 适用场景 | 用户体验 | 维护成本 | 分发方式 |
|------|---------|----------|---------|---------|
| **A. PyPI 独立发布** | 面向 Python 开发者 | `pip install` 即用 | 低 | PyPI |
| **B. Pyx 打包独立可执行文件** | 面向非技术用户 | 双击/命令行直接运行 | 中 | GitHub Releases |
| **C. Docker 镜像** | 服务端/CI 场景 | `docker run` 即用 | 低 | Docker Hub / GHCR |
| **D. 混合方案（推荐）** | 覆盖所有场景 | 按需选择 | 中 | PyPI + GitHub Releases |

---

## 方案 A：PyPI 独立发布（推荐优先执行）

### 核心思路

不改动 `markitdown` 主包名，仅将 `markitdown-glmocr` 发布到 PyPI。用户安装方式：

```bash
pip install markitdown[all] markitdown-glmocr[glmocr]
```

使用时加 `-p` 参数启用插件：

```bash
markitdown -p document.pdf
```

### 为什么不 fork 一个 `markitdown-glmocr-all` 包？

1. `markitdown` 的插件机制（entry_points）已经设计好，`markitdown-glmocr` 作为插件包完全解耦
2. 避免维护 markitdown 核心代码的 fork 副本
3. 官方更新 markitdown 核心时，用户直接 `pip install -U markitdown` 即可升级

### 详细步骤

#### 1. 修改 `markitdown-glmocr` 的 pyproject.toml

```toml
[project]
name = "markitdown-glmocr"
version = "0.1.0"  # 改为静态版本，首次发布不用 dynamic
description = "Intelligent PDF/Image to Markdown converter using GLM-OCR SDK"
readme = "README.md"
requires-python = ">=3.10"
license = "MIT"
authors = [
  { name = "Your Name", email = "your@email.com" },
]

# 关键：声明对 markitdown 的版本范围依赖
dependencies = [
  "markitdown>=0.1.0,<1.0.0",
  "pdfminer.six>=20251230",
  "pdfplumber>=0.11.9",
  "Pillow>=9.0.0",
]

[project.optional-dependencies]
glmocr = ["glmocr>=0.1.0"]
all = [
  "glmocr>=0.1.0",
  "markitdown[all]",
]
dev = ["pytest>=7.0.0", "build", "twine"]

# 插件入口点（已有，无需修改）
[project.entry-points."markitdown.plugin"]
markitdown_glmocr = "markitdown_glmocr"
```

#### 2. 编写 README.md

在 `packages/markitdown-glmocr/` 下创建完善的 README：

```markdown
# markitdown-glmocr

Intelligent PDF/Image to Markdown converter plugin for [markitdown](https://github.com/microsoft/markitdown),
powered by [GLM-OCR](https://github.com/zai-org/glm-ocr) SDK.

## Installation

pip install markitdown-glmocr[glmocr]

## Usage

# Enable plugins with -p flag
markitdown -p document.pdf
markitdown -p image.png

# Or use programmatically
from markitdown import MarkItDown
md = MarkItDown(enable_plugins=True)
result = md.convert("document.pdf")
print(result.markdown)

## Configuration

Set your Zhipu API key:

export ZHIPU_API_KEY=your_api_key_here
```

#### 3. 构建并发布

```bash
cd packages/markitdown-glmocr

# 安装构建工具
pip install build twine

# 构建 wheel 和 sdist
python -m build

# 检查包
twine check dist/*

# 上传到 TestPyPI 先验证
twine upload --repository testpypi dist/*

# 验证安装
pip install --index-url https://test.pypi.org/simple/ markitdown-glmocr[glmocr]

# 正式发布到 PyPI
twine upload dist/*
```

#### 4. PyPI 账号准备

- 注册 https://pypi.org 账号
- 配置 API Token：Account settings → API tokens → Add API token
- 配置 `~/.pypirc`：

```ini
[pypi]
username = __token__
password = pypi-xxxxxxxxxxxx

[testpypi]
username = __token__
password = pypi-test-xxxxxxxxxxxx
```

### 优缺点

| 优点 | 缺点 |
|------|------|
| 标准Python生态分发方式 | 需要用户有Python环境 |
| 插件机制天然解耦，官方更新不受影响 | glmocr SDK 依赖较多（numpy, pymupdf等） |
| 版本管理清晰 | 需要维护PyPI账号和token |
| `pip install` 一行搞定 | |

---

## 方案 B：PyInstaller 打包独立可执行文件

### 核心思路

将 markitdown + markitdown-glmocr + glmocr + 所有依赖打包成单个可执行文件，用户无需安装 Python。

### 详细步骤

#### 1. 创建打包配置

在项目根目录创建 `build_standalone/` 目录：

```
build_standalone/
├── build.py          # 构建脚本
├── markitdown.spec   # PyInstaller spec 文件
└── README.md         # 使用说明
```

#### 2. 编写 PyInstaller spec 文件

`build_standalone/markitdown.spec`：

```python
# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path

block_cipher = None

# 收集所有隐式导入的模块
hiddenimports = [
    'markitdown',
    'markitdown.converters',
    'markitdown_glmocr',
    'glmocr',
    'pdfminer',
    'pdfminer.high_level',
    'pdfminer.layout',
    'pdfminer.utils',
    'pdfplumber',
    'PIL',
    'magika',
    'charset_normalizer',
    'markdownify',
    'beautifulsoup4',
    'bs4',
    'mammoth',
    'openpyxl',
    'pandas',
    'python_pptx',
    'lxml',
    'numpy',
    'pydantic',
    'pymupdf',
    'fitz',           # pymupdf 的内部名
    'tqdm',
    'yaml',
    'dotenv',
    'requests',
    'defusedxml',
]

a = Analysis(
    ['entry_point.py'],
    pathex=[],
    binaries=[],
    datas=[
        # 包含 magika 的模型文件
        ('magika/models', 'magika/models'),
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='markitdown',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
```

#### 3. 编写入口文件

`build_standalone/entry_point.py`：

```python
"""Entry point for PyInstaller build."""
import sys
import os

# 确保插件被启用
if '-p' not in sys.argv and '--use-plugins' not in sys.argv:
    # 自动启用 glmocr 插件
    sys.argv.insert(1, '-p')

from markitdown.__main__ import main

if __name__ == '__main__':
    main()
```

#### 4. 编写构建脚本

`build_standalone/build.py`：

```python
#!/usr/bin/env python3
"""Build standalone markitdown executable with PyInstaller."""
import subprocess
import sys
import platform
import shutil
from pathlib import Path

def main():
    project_root = Path(__file__).parent.parent
    build_dir = Path(__file__).parent

    # 1. 确保依赖已安装
    print(">>> Installing dependencies...")
    subprocess.run([
        sys.executable, "-m", "pip", "install", "-e",
        str(project_root / "packages" / "markitdown[all]"),
    ], check=True)
    subprocess.run([
        sys.executable, "-m", "pip", "install", "-e",
        str(project_root / "packages" / "markitdown-glmocr[glmocr]"),
    ], check=True)
    subprocess.run([
        sys.executable, "-m", "pip", "install", "pyinstaller",
    ], check=True)

    # 2. 执行 PyInstaller
    print(">>> Building executable...")
    subprocess.run([
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        str(build_dir / "markitdown.spec"),
    ], cwd=str(build_dir), check=True)

    # 3. 输出结果
    dist_dir = build_dir / "dist"
    exe_name = "markitdown.exe" if platform.system() == "Windows" else "markitdown"
    exe_path = dist_dir / exe_name

    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"\n✅ Build successful!")
        print(f"   Executable: {exe_path}")
        print(f"   Size: {size_mb:.1f} MB")
        print(f"   Platform: {platform.system()} {platform.machine()}")
    else:
        print("\n❌ Build failed - executable not found")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

#### 5. GitHub Actions 自动构建多平台

`.github/workflows/build-standalone.yml`：

```yaml
name: Build Standalone Executable

on:
  push:
    tags: ['v*']
  workflow_dispatch:

jobs:
  build:
    strategy:
      matrix:
        include:
          - os: windows-latest
            artifact: markitdown-windows-x64.exe
          - os: ubuntu-latest
            artifact: markitdown-linux-x64
          - os: macos-latest
            artifact: markitdown-macos-x64

    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'

      - name: Install dependencies
        run: |
          pip install -e ./packages/markitdown[all]
          pip install -e ./packages/markitdown-glmocr[glmocr]
          pip install pyinstaller

      - name: Build with PyInstaller
        run: |
          pyinstaller --clean --noconfirm build_standalone/markitdown.spec
        working-directory: .

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: ${{ matrix.artifact }}
          path: dist/markitdown*

  release:
    needs: build
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/v')
    steps:
      - uses: actions/download-artifact@v4
        with:
          path: artifacts

      - name: Create Release
        uses: softprops/action-gh-release@v2
        with:
          files: artifacts/**
          generate_release_notes: true
```

### 预估产物大小

| 平台 | 预估大小 | 说明 |
|------|---------|------|
| Windows x64 | ~80-120 MB | 含 Python 运行时 + numpy + pymupdf 等 |
| Linux x64 | ~60-90 MB | |
| macOS x64 | ~70-100 MB | |

### 优缺点

| 优点 | 缺点 |
|------|------|
| 无需Python环境，双击可用 | 产物体积大（80-120MB） |
| 非技术用户友好 | 每次更新需重新打包 |
| 可离线使用 | PyInstaller 隐式导入容易遗漏，调试成本高 |
| 可通过 GitHub Releases 分发 | 跨平台需分别构建 |
| | 杀毒软件可能误报 |

### 替代方案：Nuitka

如果 PyInstaller 遇到问题，可考虑 [Nuitka](https://nuitka.net/)：

```bash
pip install nuitka
python -m nuitka --standalone --onefile \
    --enable-plugin=numpy,pandas \
    --include-data-dir=magika/models=magika/models \
    entry_point.py
```

Nuitka 编译为真正的机器码，性能更好，但构建时间更长。

---

## 方案 C：Docker 镜像

### 核心思路

基于官方 Dockerfile 扩展，加入 glmocr 插件。

### Dockerfile

```dockerfile
FROM python:3.13-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg exiftool && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY packages/markitdown /app/packages/markitdown
COPY packages/markitdown-glmocr /app/packages/markitdown-glmocr

RUN pip --no-cache-dir install \
    /app/packages/markitdown[all] \
    /app/packages/markitdown-glmocr[glmocr]

ENTRYPOINT ["markitdown"]
```

### 使用方式

```bash
# 构建
docker build -t markitdown-glmocr .

# 使用
docker run --rm -v $(pwd):/data markitdown-glmocr -p /data/document.pdf

# 发布到 GHCR
docker tag markitdown-glmocr ghcr.io/yourname/markitdown-glmocr:latest
docker push ghcr.io/yourname/markitdown-glmocr:latest
```

### 优缺点

| 优点 | 缺点 |
|------|------|
| 环境完全隔离 | 需要 Docker 环境 |
| 适合 CI/CD 集成 | 镜像体积 ~500MB+ |
| 服务端部署友好 | 桌面用户不友好 |

---

## 方案 D：混合方案（推荐）

### 执行优先级

```
1️⃣ 方案A：PyPI 发布 markitdown-glmocr    →  Python 开发者首选
2️⃣ 方案B：PyInstaller 打包               →  非技术用户 / 离线场景
3️⃣ 方案C：Docker 镜像                    →  服务端 / CI 场景（可选）
```

### 具体执行计划

#### Phase 1：PyPI 发布（1-2 天）

1. **完善 markitdown-glmocr 包**
   - [ ] 补充 README.md（安装、使用、配置说明）
   - [ ] 补充 LICENSE 文件
   - [ ] 添加 `py.typed` 标记（如需类型提示支持）
   - [ ] 修复 `__about__.py` 版本号为 `0.1.0`
   - [ ] 确保所有依赖版本范围合理

2. **本地验证**
   - [ ] 在全新虚拟环境中测试安装流程
   ```bash
   python -m venv /tmp/test-env
   source /tmp/test-env/bin/activate
   pip install markitdown[all] markitdown-glmocr[glmocr]
   markitdown -p --list-plugins  # 应显示 markitdown_glmocr
   markitdown -p test.pdf        # 功能测试
   ```

3. **发布到 TestPyPI 验证**
   - [ ] `python -m build`
   - [ ] `twine upload --repository testpypi dist/*`
   - [ ] 从 TestPyPI 安装并测试

4. **正式发布到 PyPI**
   - [ ] `twine upload dist/*`

5. **发布后验证**
   - [ ] `pip install markitdown-glmocr[glmocr]`
   - [ ] 功能测试通过

#### Phase 2：独立可执行文件（2-3 天）

1. **搭建 PyInstaller 构建流程**
   - [ ] 创建 `build_standalone/` 目录和配置
   - [ ] 本地 Windows 构建测试
   - [ ] 解决隐式导入问题（最耗时）

2. **GitHub Actions CI/CD**
   - [ ] 配置多平台构建 workflow
   - [ ] 打 tag 触发自动构建和 Release

3. **分发**
   - [ ] GitHub Releases 页面提供下载
   - [ ] README 中添加下载链接

#### Phase 3：Docker 镜像（可选，0.5 天）

1. **编写 Dockerfile**
2. **发布到 GHCR**
3. **文档补充**

---

## 关于 PR 合并的判断

### 官方接受 PR 的可能性分析

| 因素 | 评估 |
|------|------|
| markitdown 已有插件机制 | ✅ 架构上完全兼容 |
| glmocr 是第三方商业API | ⚠️ 官方可能不愿绑定特定商业服务 |
| 官方已有 azure-doc-intel 集成 | ✅ 有先例，但 Azure 是微软自家产品 |
| PR 贡献者不是微软员工 | ⚠️ 可能需要较长时间审核 |
| markitdown 版本还在 0.x (Beta) | ✅ 正是引入新功能的阶段 |

**结论**：官方大概率不会直接接受 glmocr 插件 PR（因为绑定了非微软的商业 API），但插件机制的存在意味着**不需要官方接受 PR**，独立发布到 PyPI 是完全合理的路径。

### 建议策略

1. **先独立发布到 PyPI**（方案A），不依赖官方
2. **同时提交 PR**，作为"贡献回社区"的姿态，即使被拒也无所谓
3. PR 描述中强调：
   - 完全通过插件机制扩展，不修改核心代码
   - 可作为"第三方插件集成"的参考实现
   - 有完整的测试和文档

---

## 快速开始：5分钟发布到 PyPI

如果你现在就想发布，执行以下命令：

```bash
# 1. 进入 glmocr 插件目录
cd D:/15-AI-Coding/markitdown/packages/markitdown-glmocr

# 2. 安装构建工具
pip install build twine

# 3. 构建
python -m build

# 4. 检查
twine check dist/*

# 5. 发布到 TestPyPI（先测试）
twine upload --repository testpypi dist/*

# 6. 确认无误后发布到正式 PyPI
twine upload dist/*
```

发布后，其他人只需：

```bash
pip install markitdown-glmocr[glmocr]
export ZHIPU_API_KEY=your_key
markitdown -p your-file.pdf
```

---

## 附录：常见问题

### Q1: 用户不装 glmocr SDK，只装 markitdown-glmocr 会怎样？

不会报错。`_converter.py` 中 glmocr 是 lazy import，只在实际转换时才检查。
但建议用户安装 `markitdown-glmocr[glmocr]` 以获得完整功能。

### Q2: 如何处理 markitdown 核心包的版本兼容性？

`markitdown-glmocr` 的 `pyproject.toml` 中声明 `markitdown>=0.1.0,<1.0.0`。
markitdown 的插件接口（entry_points）是稳定的，0.x 版本间不会 breaking change。

### Q3: PyInstaller 打包后 API Key 如何配置？

通过环境变量 `ZHIPU_API_KEY` 传入，或在运行时通过 `.env` 文件：
```bash
# 方式1：环境变量
set ZHIPU_API_KEY=your_key
markitdown -p document.pdf

# 方式2：.env 文件（glmocr SDK 自动读取）
echo ZHIPU_API_KEY=your_key > .env
markitdown -p document.pdf
```

### Q4: 能否做一个"一键安装包"给非技术用户？

可以结合 PyInstaller + Inno Setup（Windows）或 create-dmg（macOS）做安装向导：

```
Windows: PyInstaller → .exe → Inno Setup → .exe 安装向导
macOS:   PyInstaller → binary → create-dmg → .dmg
Linux:   PyInstaller → binary → AppImage → .AppImage
```

但这增加了维护成本，建议先只提供裸 executable，待有需求再加安装向导。

### Q5: uvx / pipx 支持吗？

支持！发布到 PyPI 后：

```bash
# 一次性运行（无需安装）
uvx --from markitdown-glmocr[glmocr] markitdown -p document.pdf

# 或用 pipx
pipx run markitdown -p document.pdf
```

这是最推荐的非技术用户使用方式——比 PyInstaller 更轻量，且始终使用最新版。
