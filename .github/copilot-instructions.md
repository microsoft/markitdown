# Copilot Coding Agent Instructions

## Mandatory Workflow (MUST follow in order)

### Phase 1: Reproduce (MUST complete before Phase 2)
- Read the issue description and understand the problem.
- Write a failing test or run the existing test suite to confirm the bug.
- **Do NOT proceed to Phase 2 until you have a confirmed failure.**

### Phase 2: Implement (MUST complete before Phase 3)
- Make the minimal code change to fix the bug.
- Do NOT refactor unrelated code or add features.

### Phase 3: Verify (MUST complete before committing)
- Re-run the specific test from Phase 1 and confirm it passes.
- Run the full test suite to check for regressions.
- **Do NOT commit until all tests pass.**

## Rules
- DO NOT reference, close, or link any external issues. No Closes, Fixes, or Resolves directives.
- DO NOT use GitHub MCP tools to look up issues on other repositories.
- DO NOT modify or weaken a test to make it pass.
- DO NOT commit __pycache__/ directories. Add to .gitignore if missing.
- Keep changes minimal and focused.
