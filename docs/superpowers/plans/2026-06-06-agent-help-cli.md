# Agent Help CLI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `--agent-help` to the `markitdown` CLI without changing conversion, plugin listing, version, or normal error outputs.

**Architecture:** Keep the CLI in `packages/markitdown/src/markitdown/__main__.py`, matching the existing single-file argparse structure. Add a hidden argparse flag and a small AHF emitter that exits before any conversion work. Keep runtime output handling untouched.

**Tech Stack:** Python 3.10+, argparse, pytest, subprocess-based CLI tests.

---

## File Structure

- Modify `packages/markitdown/tests/test_cli_misc.py`: add subprocess tests for the help breadcrumb and `--agent-help` AHF output.
- Modify `packages/markitdown/src/markitdown/__main__.py`: add a hidden `--agent-help` argparse flag, append the human-help breadcrumb, and emit stable AHF output before parsing conversion hints or reading stdin.

## Task 1: Add Failing CLI Coverage

**Files:**
- Modify: `packages/markitdown/tests/test_cli_misc.py`
- Test: `packages/markitdown/tests/test_cli_misc.py`

- [ ] **Step 1: Write failing tests**

Add these tests after `test_version`:

```python
def test_help_includes_agent_help_breadcrumb() -> None:
    result = subprocess.run(
        ["python", "-m", "markitdown", "--help"], capture_output=True, text=True
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    assert (
        "LLM agent? Use --agent-help for token-optimized usage." in result.stdout
    )


def test_agent_help_outputs_ahf_without_running_conversion() -> None:
    result = subprocess.run(
        ["python", "-m", "markitdown", "--agent-help"],
        input="plain text that must not be converted",
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    assert result.stderr == ""
    assert result.stdout.startswith("ah1 markitdown :: convert files and streams to markdown\n")
    assert "cmd markitdown [filename] [--output path] [--extension str] [--mime-type str] [--charset str] :: convert input to markdown" in result.stdout
    assert "more? markitdown --agent-help" in result.stdout
    assert "ah2 markitdown" in result.stdout
    assert "use markitdown [filename] [--output path] [--extension str] [--mime-type str] [--charset str]" in result.stdout
    assert "arg filename:path opt :: input file path; omit to read from stdin" in result.stdout
    assert "flag --use-docintel:bool opt :: use Azure Document Intelligence; requires --endpoint and filename" in result.stdout
    assert "flag --use-cu:bool opt :: use Azure Content Understanding; requires --cu-endpoint and filename" in result.stdout
    assert "ex markitdown example.pdf -o example.md" in result.stdout
    assert "plain text that must not be converted" not in result.stdout
```

- [ ] **Step 2: Run tests to verify they fail**

Run from `packages/markitdown`:

```powershell
uv run --with pytest --with-editable . python -m pytest tests/test_cli_misc.py -k "agent_help or breadcrumb" -v
```

Expected: the new tests fail because `--agent-help` is not recognized and the breadcrumb is absent.

## Task 2: Implement `--agent-help`

**Files:**
- Modify: `packages/markitdown/src/markitdown/__main__.py`
- Test: `packages/markitdown/tests/test_cli_misc.py`

- [ ] **Step 1: Add the hidden argparse flag and breadcrumb**

In `main()`, add this to the parser description or epilog through argparse so normal `--help` includes the breadcrumb:

```python
epilog="LLM agent? Use --agent-help for token-optimized usage.",
```

Add this parser argument before `parse_args()`:

```python
parser.add_argument(
    "--agent-help",
    action="store_true",
    help=argparse.SUPPRESS,
)
```

- [ ] **Step 2: Add a stable AHF emitter**

Add this helper near the other private helpers:

```python
def _print_agent_help() -> None:
    print(
        "\n".join(
            [
                "ah1 markitdown :: convert files and streams to markdown",
                "cmd markitdown [filename] [--output path] [--extension str] [--mime-type str] [--charset str] :: convert input to markdown",
                "more? markitdown --agent-help",
                "ah2 markitdown",
                "use markitdown [filename] [--output path] [--extension str] [--mime-type str] [--charset str]",
                "arg filename:path opt :: input file path; omit to read from stdin",
                "flag --output:path opt :: write markdown to file instead of stdout",
                "flag --extension:str opt :: input extension hint, with or without leading dot",
                "flag --mime-type:str opt :: input MIME type hint",
                "flag --charset:str opt :: input charset hint",
                "flag --use-plugins:bool opt :: enable installed third-party plugins",
                "flag --list-plugins:bool opt :: list installed third-party plugins and exit",
                "flag --keep-data-uris:bool opt :: keep base64 data URIs in markdown output",
                "flag --use-docintel:bool opt :: use Azure Document Intelligence; requires --endpoint and filename",
                "flag --endpoint:url opt :: Azure Document Intelligence endpoint",
                "flag --use-cu:bool opt :: use Azure Content Understanding; requires --cu-endpoint and filename",
                "flag --cu-endpoint:url opt :: Azure Content Understanding endpoint",
                "flag --cu-analyzer:str opt :: Azure Content Understanding analyzer ID",
                "flag --cu-file-types:str opt :: comma-separated file types routed to Content Understanding",
                "ex markitdown example.pdf",
                "ex markitdown example.pdf -o example.md",
                "ex cat example.html | markitdown --extension html",
            ]
        )
    )
```

- [ ] **Step 3: Exit before conversion when requested**

Immediately after `args = parser.parse_args()`, add:

```python
if args.agent_help:
    _print_agent_help()
    sys.exit(0)
```

- [ ] **Step 4: Run focused tests**

Run from `packages/markitdown`:

```powershell
uv run --with pytest --with-editable . python -m pytest tests/test_cli_misc.py -k "agent_help or breadcrumb" -v
```

Expected: the focused tests pass.

## Task 3: Guard Existing Surfaces

**Files:**
- Modify: `packages/markitdown/tests/test_cli_misc.py`
- Test: `packages/markitdown/tests/test_cli_misc.py`

- [ ] **Step 1: Add explicit regression checks**

Add this test near `test_invalid_flag`:

```python
def test_invalid_flag_keeps_argparse_error_surface() -> None:
    result = subprocess.run(
        ["python", "-m", "markitdown", "--foobar"], capture_output=True, text=True
    )

    assert result.returncode != 0, f"CLI exited with error: {result.stderr}"
    assert "unrecognized arguments" in result.stderr
    assert "SYNTAX" in result.stderr
    assert not result.stderr.startswith("err ")
```

If this duplicates existing `test_invalid_flag`, update the existing test with only the final assertion instead of adding a separate test.

- [ ] **Step 2: Run CLI misc tests**

Run from `packages/markitdown`:

```powershell
uv run --with pytest --with-editable . python -m pytest tests/test_cli_misc.py -v
```

Expected: all CLI misc tests pass.

## Task 4: Verify Full Relevant Suite

**Files:**
- No code changes unless verification exposes a regression.

- [ ] **Step 1: Run package tests**

Run from `packages/markitdown`:

```powershell
uv run --with pytest --with-editable . python -m pytest tests -v
```

Expected: all local tests pass or only pre-existing environment/dependency issues are reported with exact evidence.

- [ ] **Step 2: Manually verify command surfaces**

Run from `packages/markitdown`:

```powershell
uv run --with-editable . python -m markitdown --help
uv run --with-editable . python -m markitdown --agent-help
uv run --with-editable . python -m markitdown --version
```

Expected: help includes the breadcrumb, agent-help emits AHF, and version output remains unchanged.

- [ ] **Step 3: Review final diff**

Run from repo root:

```powershell
git diff --stat
git diff
```

Expected: only the spec, plan, CLI module, and CLI misc tests changed.
