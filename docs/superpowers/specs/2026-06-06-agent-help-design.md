# Agent Help Design

## Goal

Add agent-help invocation guidance to the `markitdown` CLI so LLM agents can discover the supported command shape without parsing human help text.

## Scope

This change adds only `--agent-help` support to the primary `markitdown` command in `packages/markitdown`. It must preserve every existing runtime output surface:

- Normal conversion to stdout remains markdown-only.
- `-o/--output` continues writing only the converted markdown to the requested file.
- `--list-plugins` keeps its current human-readable output.
- `--help`, invalid argument handling, and `--version` keep existing argparse behavior except for the new help breadcrumb.

This change intentionally does not add `--agent-out`, JSON output, TOON runtime envelopes, or structured conversion results.

## User-Facing Behavior

`markitdown --help` appends this breadcrumb:

```text
LLM agent? Use --agent-help for token-optimized usage.
```

`markitdown --agent-help` exits successfully and emits AHF plain text. Because `markitdown` is a single-command CLI with no subcommands, the output contains both a compact AH1 index and enough AH2-style detail for the root conversion command. This avoids inventing a fake subcommand solely for command detail.

The AHF output covers:

- The command purpose.
- The optional `filename` argument.
- The canonical invocation.
- Material flags that change conversion behavior, including output, type hints, plugin loading, cloud conversion modes, and data URI handling.
- Valid examples that work without external services.

`--agent-help` is hidden from normal argparse option listings except for the breadcrumb. It does not require input and does not run a conversion.

## Architecture

Keep the implementation local to `packages/markitdown/src/markitdown/__main__.py` because the existing CLI is a compact argparse module. Add helpers that build the parser, emit agent-help text, and run the conversion. This keeps tests able to invoke the real module through `python -m markitdown`.

Use argparse metadata for normal option behavior and a concise AHF string for the agent-facing surface. The AHF string should be stable, ASCII-only, and short enough for agent invocation discovery.

## Testing

Add CLI tests in `packages/markitdown/tests/test_cli_misc.py` for:

- `--help` includes the breadcrumb.
- `--agent-help` exits successfully and emits AH1/AH2 records, command usage, key flags, and no markdown/prose formatting.
- `--agent-help` does not require input conversion.
- Existing invalid flag behavior remains argparse-compatible without `--agent-help`.

No test should require network access or cloud credentials. Existing CLI vector tests should continue to prove conversion output is unchanged.
