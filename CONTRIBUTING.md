# Contributing to MarkItDown

Thank you for your interest in contributing to MarkItDown! This guide explains how to set up your development environment, run tests, and submit changes.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setting Up the Dev Environment](#setting-up-the-dev-environment)
- [Running Checks and Tests](#running-checks-and-tests)
- [Making Changes](#making-changes)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Code of Conduct](#code-of-conduct)

---

## Prerequisites

- **Python 3.10+** (3.12 recommended)
- **git**
- A virtual environment tool (`venv`, `uv`, or `conda`)

---

## Setting Up the Dev Environment

### 1. Fork and clone the repository

```bash
git clone https://github.com/<your-username>/markitdown.git
cd markitdown
```

### 2. Create a virtual environment

**Using `venv`** (standard library):

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate      # Windows
```

**Using `uv`** (faster):

```bash
uv venv --python=3.12 .venv
source .venv/bin/activate
```

**Using `conda`**:

```bash
conda create -n markitdown python=3.12
conda activate markitdown
```

### 3. Install the package in editable mode with all optional dependencies

```bash
pip install -e 'packages/markitdown[all]'
```

To install only the packages you need for your change (faster):

```bash
pip install -e 'packages/markitdown[pdf,docx]'   # example: PDF and Word only
```

### 4. (Optional) Install the MCP package

If your change involves the MCP integration:

```bash
pip install -e packages/markitdown-mcp
```

---

## Running Checks and Tests

All tests live under `packages/markitdown/tests/`.

### Run the full test suite

```bash
cd packages/markitdown
python -m pytest tests/ -v
```

### Run a single test file

```bash
python -m pytest tests/test_markitdown.py -v
```

### Run tests matching a keyword

```bash
python -m pytest tests/ -k "pdf" -v
```

### Lint / style checks

MarkItDown uses standard Python tooling. Before opening a PR, please verify your code passes:

```bash
# Type checking (if you have pyright or mypy installed)
pyright packages/markitdown/src

# Or with mypy
mypy packages/markitdown/src
```

---

## Making Changes

1. Create a feature branch from `main`:

   ```bash
   git checkout -b fix/my-descriptive-branch-name
   ```

2. Make your changes inside `packages/markitdown/src/markitdown/`.

3. Add or update tests in `packages/markitdown/tests/` to cover your change.

4. Run the test suite (see above) and ensure all tests pass.

5. Commit with a clear message:

   ```bash
   git commit -m "fix: describe what you changed and why"
   ```

---

## Submitting a Pull Request

1. Push your branch to your fork:

   ```bash
   git push origin fix/my-descriptive-branch-name
   ```

2. Open a pull request against `microsoft/markitdown:main`.

3. Fill in the PR description — briefly explain **what** changed and **why**.

4. Reference any related issue (e.g., `Closes #6`).

A maintainer will review your PR as soon as possible. Please be patient; this is an actively maintained open-source project.

---

## Code of Conduct

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details.
