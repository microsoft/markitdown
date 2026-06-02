# Contributing to MarkItDown

Thank you for helping improve MarkItDown. This guide covers the local setup,
test commands, and pull request checklist that maintainers need contributors to
run before review.

## Development Setup

MarkItDown is a Python monorepo. The core package lives in
`packages/markitdown`, with related packages in sibling directories such as
`packages/markitdown-mcp`, `packages/markitdown-ocr`, and
`packages/markitdown-sample-plugin`.

Use Python 3.10 or newer. Python 3.12 is a good default for local development.

```sh
git clone https://github.com/microsoft/markitdown.git
cd markitdown
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install hatch pre-commit
```

On Windows, activate the virtual environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the core package in editable mode when you want to run the CLI or
exercise changes manually:

```sh
python -m pip install -e 'packages/markitdown[all]'
```

If you are working on one optional format, you can install only that extra to
keep setup smaller. For example:

```sh
python -m pip install -e 'packages/markitdown[pdf,docx]'
```

If your change is in another package, install that package from its directory or
path as well:

```sh
python -m pip install -e packages/markitdown-mcp
python -m pip install -e packages/markitdown-ocr
```

## Running Tests and Checks

Run commands from the package you are changing unless noted otherwise.

For the core package:

```sh
cd packages/markitdown
hatch test
```

Run one test file or one test case with `pytest` through Hatch:

```sh
hatch run pytest tests/test_module_misc.py -v
hatch run pytest tests/test_module_misc.py::test_exceptions -v
```

Run type checks for the core package:

```sh
hatch run types:check
```

For related packages, use their own test suite:

```sh
cd packages/markitdown-mcp
hatch test

cd ../markitdown-ocr
hatch test
```

Before opening a pull request, run pre-commit from the repository root:

```sh
pre-commit run --all-files
```

## Pull Request Checklist

- Keep the pull request focused on one bug fix, feature, or documentation
  improvement.
- Add or update tests for code changes when practical.
- Update documentation when behavior, installation, or supported formats change.
- Mention related issues in the PR body, for example `Closes #123`.
- Include the exact commands you ran under a `Test Plan` or `Verification`
  section.
- Respond to the Microsoft CLA bot if it asks you to sign the Contributor
  License Agreement.

## Security

MarkItDown performs I/O with the privileges of the current process. For changes
that touch local paths, URIs, archives, or server/MCP behavior, keep the
repository's security guidance in mind and prefer the narrowest conversion API
that fits the use case.

Report security issues through the process in [SECURITY.md](SECURITY.md), not in
public GitHub issues.

## Community

This project follows the [Microsoft Open Source Code of Conduct](CODE_OF_CONDUCT.md).
