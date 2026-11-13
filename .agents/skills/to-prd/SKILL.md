---
name: to-prd
description: Turn the current conversation context into a PRD and publish it to the project issue tracker. Use when user wants to create a PRD from the current context.
---

This skill takes the current conversation context and codebase understanding and produces a PRD. Do NOT interview the user - just synthesize what you already know.

The issue tracker and triage label vocabulary should have been provided to you - run `/setup-matt-pocock-skills` if not.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the PRD, and respect any ADRs in the area you're touching.

2. Sketch out the major modules you will need to build or modify to complete the implementation. Actively look for opportunities to extract deep modules that can be tested in isolation.

A deep module (as opposed to a shallow module) is one which encapsulates a lot of functionality in a simple, testable interface which rarely changes.

Check with the user that these modules match their expectations. Check with the user which modules they want tests written for.

<!-- 3. Write the PRD using the template below. Use the domain language from `CONTEXT.md` and ADRs to make the PRD as precise as possible. -->

3. Write the PRD using the template in `PRD.md` (in this skill directory), then publish it to the project issue tracker. Apply the `ready-for-agent` triage label - no need for additional triage. Use the domain language from `CONTEXT.md` and ADRs to make the PRD as precise as possible.

   Two diagrams are required (both Mermaid, so the tracker's markdown renders them): a **class diagram** in Module Breakdown showing the modules/classes and their relationships, and a **sequence diagram** in Control Flow & Interactions showing how they interact at runtime. Do not skip them because the feature "looks simple" - the diagrams are the fastest way for an implementing agent to grasp structure and flow.

4. Check for a repo-local PRD extension at `.claude/skills/to-prd.md` in the project root. If it exists, apply its additional requirements (extra sections, extra diagrams, project conventions) on top of the `PRD.md` template. Most repos won't have one - only apply it when present.
