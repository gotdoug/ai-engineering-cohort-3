---
name: execplan-from-phase-scope
description: Creates a new ExecPlan from a plan phase scope using the multi-agent workflow guide. Use when the user wants to expand a phase scope document into a detailed, executable plan with agent coordination, granular steps, checkpoints, and validation criteria.
---

# ExecPlan from Phase Scope

Expands a brief phase scope (e.g., `phase-0-validate-prerequisites.md`) into a full ExecPlan that follows MULTI_AGENT_WORKFLOW_GUIDE.md. Outputs a self-contained, novice-guiding, outcome-focused plan with agent-specific steps.

## When to Use

- User asks to create an ExecPlan from a phase scope
- User wants to turn a plan-of-work phase into a detailed implementation plan
- User references "multi-agent workflow" and a phase document together

## Workflow

```
Phase scope → Read MULTI_AGENT_WORKFLOW_GUIDE → Produce ExecPlan
```

## Step 1: Gather Inputs

Read these files (paths from repository root):

1. **Phase scope** — The brief phase document (e.g., `capstone/voice-dictation/plan-of-work/phase-N-*.md`)
2. **MULTI_AGENT_WORKFLOW_GUIDE.md** — Multi-agent structure, agent roles, checkpoints, granular steps

Also read any parent implementation plan that provides context (e.g., `voice-dictation-macos-implementation-plan.md`).

## Step 2: Extract from Phase Scope

From the phase scope, capture:

- **Purpose** — What the phase proves or delivers
- **Scope** — Concrete tasks (numbered list, bullets)
- **Acceptance** — What “done” looks like
- **Technical hints** — Platforms, tools, APIs mentioned

## Step 3: Structure the ExecPlan

Follow MULTI_AGENT_WORKFLOW_GUIDE.md. Include:

**Workflow Orchestration and Agent Coordination**
- Initial Trigger (Human Action)
- Agent Execution Sequence (who does what, in order)
- Agent Communication Protocol (Git, PRs, checkpoints)
- Work Tree Management (if applicable)
- Error Handling and Recovery
- Automation Requirements

**Concrete Steps with Agent-Specific Granularity**
- Step numbering (Step X.Y) for each agent
- Exact commands, file paths, working directories
- Expected output or success indicators

**Progress, Validation, and Recovery**
- Progress section with checkboxes for every step
- Validation and Acceptance (per-agent and overall)
- Idempotence and Recovery

**Task checkoff (mandatory):** The plan must state that as each task is completed, the executing agent updates the Progress section by changing `- [ ]` to `- [x]` for that task. The document is a living record; checkoffs keep it current.

## Step 4: Add Task Checkoff Requirement

The ExecPlan must explicitly instruct agents to **check off completed tasks in the Progress section**. Include this instruction in the document:

- When an agent completes a step, it must update the corresponding Progress checkbox from `- [ ]` to `- [x]`.
- Optionally: add timestamp (e.g., `- [x] (2025-01-31 14:00Z) Agent 1: Step 1.1 — ...`).
- The plan is a living document; checkoffs reflect current state and enable resumption from any checkpoint.

## Step 5: Assign Agents and Steps

Break phase scope into agent responsibilities:

- **Development Agent** — Implementation, code, build, commit
- **Verification Agent** — Run, validate, document outcomes
- **Code Review Agent** — Optional; use if phase merits review
- **Plan Alignment Agent** — Optional; use if verifying against parent plan

For spikes or small phases, Development + Verification is often enough.

**Step numbering:** Use `Step X.Y` (e.g., Step 1.1, 1.2, 2.1). Each step must be self-contained.

## Step 6: Add Granular Detail

For each step, include:

- **Working directory** — Where to run commands
- **Exact commands** — With placeholders (`$VAR`, `<path>`) where needed
- **Expected output** — Short transcript or success indicator
- **File paths** — Full repository-relative paths
- **Checkpoints** — What signals completion before the next agent starts

## Step 7: Define Acceptance

For each agent’s completion:

- What must be true (e.g., “Spike builds and runs”)
- Observable behavior (e.g., “Text appears in TextEdit without manual paste”)
- How to verify (commands to run, what to observe)

## Step 8: Output

Write the ExecPlan to the plan-of-work directory. Naming convention:

- `phase-N-<phase-name>-execplan.md` (e.g., `phase-0-validate-prerequisites-execplan.md`)

Place it alongside the original phase scope in the same directory.

## Output Template

```markdown
# Phase N: [Phase Name] — [Short Description] (ExecPlan)

This ExecPlan is a living document. The sections Progress, Surprises & Discoveries, Decision Log, and Outcomes & Retrospective must be kept up to date.

This document follows MULTI_AGENT_WORKFLOW_GUIDE.md at the repository root. As tasks are completed, update the Progress section: change `- [ ]` to `- [x]` for that task.

---

## Purpose / Big Picture
[2-4 sentences: what succeeds, how to see it working]

## Progress

*As each task completes, check it off: change `- [ ]` to `- [x]`.*

- [ ] Agent 1: Step 1.1 — [task]
- [ ] Agent 1: Step 1.2 — [task]
- [ ] Agent 2: Step 2.1 — [task]
...

## Surprises & Discoveries
*(None yet.)*

## Decision Log
- Decision: ...
  Rationale: ...
  Date/Author: ...

## Outcomes & Retrospective
*(To be filled when complete.)*

## Context and Orientation
[Source documents, terms, relevant background]

## Workflow Orchestration and Agent Coordination
[Initial trigger, agent sequence, communication, work trees, error handling]

## Plan of Work
[Prose description of edits and additions]

## Concrete Steps
### Agent 1 (Development)
**Step 1.1** — [task]
Working directory: ...
[Exact commands, expected output]

### Agent 2 (Verification)
**Step 2.1** — [task]
...

## Validation and Acceptance
[Per-agent and overall acceptance criteria]

## Idempotence and Recovery
[Repeatability, rollback, cleanup]

## Artifacts and Notes
[Key paths, example transcripts]

## Interfaces and Dependencies
[Libraries, APIs, key types]
```

## Guidelines

- **Check off tasks:** Every ExecPlan must instruct agents to update Progress checkboxes as tasks complete. The document is a living record of work done.
- **Self-contained:** The ExecPlan must be usable by a novice with only this file and the repo.
- **Prose-first:** Use sentences; avoid long checklists except in Progress.
- **Embed knowledge:** Don’t link to external blogs; summarize needed info in the plan.
- **Resolve ambiguity:** Make decisions in the plan and explain why.
- **Outcome-focused:** Acceptance is observable behavior, not internal attributes.

## Reference Example

In this repo, see the transition from brief scope to full ExecPlan:

- **Phase scope:** `capstone/voice-dictation/plan-of-work/phase-0-validate-prerequisites.md` (brief)
- **ExecPlan:** `capstone/voice-dictation/plan-of-work/phase-0-validate-prerequisites-execplan.md` (full)
