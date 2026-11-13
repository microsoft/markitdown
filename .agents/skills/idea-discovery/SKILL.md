---
name: idea-discovery-with-docs
description: Collaborative discovery session that explores an idea in depth to build a complete understanding of the idea. Challenges the idea against the existing domain model, clarifies and standardises terminology, and continuously updates project knowledge through CONTEXT.md and new supporting documents. Captures requirements, domain knowledge, architectural drivers, assumptions, constraints, trade-offs, and key decisions that will influence architecture design, detailed design, implementation, and testing activities. Use when user wants to transform a high-level idea into a well-understood, documented, and traceable foundation for subsequent engineering phases.
---

<what-to-do>

Interview me relentlessly about every aspect of this idea until we have the detailed understanding in mind and the shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. The next question should be linked to the last question if possible. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing.

**Always keep that in mind**: When reporting information to me, be extremely concise and sacrifice grammar for sake of concision. Use English words/sentences at B2 or lower level to maximize clarity.

</what-to-do>

<supporting-info>

## Domain awareness

During codebase exploration, also look for existing documentation:

### File structure

Most repos have a single context:

```
/
├── CONTEXT.md
├── docs/
│   └── idea-xxxx/
│       ├── 0001-requirements-xxxx.md
|       ├── 0002-decision-xxxx.md
|       └── 0003-risk-xxxx.md
└── src/
```

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Update CONTEXT.md inline

When a term is resolved, update `CONTEXT.md` right there. Don't batch these up — capture them as they happen. Use the format in [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

`CONTEXT.md` should be totally devoid of implementation details. Do not treat `CONTEXT.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Record immediately

When a decision, assumption, constraint, or trade-off is resolved, capture it immediately in a dedicated document under `docs/idea/`.

Documentation should be concise and focused on the key points. Avoid lengthy prose and unnecessary details. Use bullet points, tables, and diagrams where appropriate to enhance clarity and readability. Use English words/sentences at B2 or lower language level to ensure understanding. Avoid idoms, jargon, and technical terms where possible.

Suggested document types:

* `requirements-xxxx.md` for requirement and domain discovery, formatted according to [REQUIREMENTS-FORMAT.md](./REQUIREMENTS-FORMAT.md)
* `decision-xxxx.md` for considered solutions, important decisions and trade-offs, formatted according to [DECISION-FORMAT.md](./DECISION-FORMAT.md)
* `risk-xxxx.md` for identified risks and open questions, formatted according to [RISK-FORMAT.md](./RISK-FORMAT.md)
* `scenario-xxxx.md` for important scenarios that influence design and testing, formatted according to [SCENARIO-FORMAT.md](./SCENARIO-FORMAT.md)
* `assumption-xxxx.md` for assumptions and constraints that influence design and testing, formatted according to [ASSUMPTION-FORMAT.md](./ASSUMPTION-FORMAT.md)
* `validation-xxxx.md` for validation plans that influence testing, formatted according to [VALIDATION-FORMAT.md](./VALIDATION-FORMAT.md)

### Document priority

When new information is discovered:

1. If it defines a domain concept, update CONTEXT.md.
2. If it introduces a requirement, update requirements-xxxx.md.
3. If it describes a real-world interaction or workflow, update scenario-xxxx.md.
4. If it introduces an assumption or constraint, update assumption-xxxx.md.
5. If it identifies uncertainty or potential failure, update risk-xxxx.md.
6. If it evaluates alternatives or resolves a design direction, update decision-xxxx.md.
7. If it requires proof or experimentation, update validation-xxxx.md.

Avoid duplicating information across documents.

</supporting-info>
