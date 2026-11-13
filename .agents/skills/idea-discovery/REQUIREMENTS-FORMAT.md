# requirements-xxxx.md

## Job of this doc

WHAT must be built + WHEN it is done. A reader must understand the problem and
the done-bar without opening any decision doc. Keep design OUT (no toolchain, no
module structure, no algorithm) - that lives in decision-xxxx.md.

Test: could another engineer design a *different valid solution* from this doc,
and know when they are finished? If they can rebuild the design from it, you
leaked too much.

## Problem / trigger

The problem and why this work exists now. Solution-free.

## Actors & use cases

WHO uses this and for WHAT. Use cases drive the requirements (esp. the NFRs), so
name them concretely.

| Actor | Use case | Drives |
| ----- | -------- | ------ |

## Functional requirements

WHAT the system must DO. One capability each, stated solution-free.

### FR-001

Description:

Rationale:

Priority:

### FR-002

Description:

Rationale:

Priority:

## Non-functional requirements

Qualities: performance, determinism, safety, "must not break X". Each needs a
testable acceptance criterion, else it is a wish not a requirement.

### NFR-001

Description:

Acceptance Criteria:

### NFR-002

Description:

Acceptance Criteria:

## Acceptance criteria (DONE bar)

The measurable bar that says the work is finished. A reader checks these to judge
done-ness. If detail lives in a validation doc, summarize + link it here.

## Scope

### In Scope

### Out of Scope

## Glossary

Key terms a reader needs, so the doc reads in one pass with no jumps elsewhere.

| Concept | Description |
| ------- | ----------- |

## Dependencies

External things assumed present (tools, libraries, other systems, prior work).

## Related (decisions = HOW)

Link the decision docs that say HOW. Do not copy their content here.
