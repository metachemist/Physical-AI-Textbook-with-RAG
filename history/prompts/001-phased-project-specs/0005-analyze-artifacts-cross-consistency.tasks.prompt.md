---
id: "0005"
title: analyze-artifacts-cross-consistency
stage: tasks
date: 2026-03-14
surface: claude-code
model: claude-sonnet-4-6
feature: 001-phased-project-specs
branch: specification
user: metachemist
command: /sp.analyze
labels: [analyze, consistency, constitution, spec, plan, tasks]
links:
  spec: specs/1-specify/spec.md
  ticket: ""
  adr: ""
  pr: ""
files:
  - path: specs/3-tasks/tasks.md
    action: read
  - path: specs/1-specify/spec.md
    action: read
  - path: specs/2-plan/plan.md
    action: read
  - path: constitution.md
    action: read
tests:
  - n/a (read-only analysis)
---

## Prompt

/sp.analyze — cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md after task generation.

Read-only analysis of: specs/1-specify/spec.md, specs/2-plan/plan.md, specs/3-tasks/tasks.md (85 tasks), constitution.md.

## Response snapshot

Produced 14 findings across all severity levels. Key results:

**CRITICAL (2):**
- F1: Constitution mandates "OpenAI Agents SDK" as required stack; plan/tasks implement agents as raw Python strategy classes using httpx/OpenRouter. No task references the SDK. Affects tasks T061–T064 and backend/pyproject.toml (T002).
- F2: Golden evaluation set tasks (T070–T071) placed in Phase 16 (Polish/Demo) but spec requires golden set complete BEFORE Phase 3 begins (Phase 2 exit criterion). Violates the hard phase gate.

**HIGH (4):**
- F3: Constitution says "30/30 answered" but spec SC-002 says "≥27/30 grounded" — different metrics and thresholds.
- F4: Constitution Judging Evidence Matrix references wrong file paths (frontend/book/, backend/api/app/routers/) vs plan/tasks paths (frontend/src/, backend/app/api/).
- F5: Constitution's personalize endpoint contract shows client sending profile in request body; plan/tasks derive track server-side from stored user_profiles.
- F6: Constitution latency targets (4000ms personalize, 4500ms agents) conflict with spec/tasks (5000ms p95 for both).

**MEDIUM (5):** Demo segment timing mismatch, translation auth inconsistency, missing ErrorResponse middleware task, session window size ambiguity across three documents, conversationId vs session_id field naming.

**LOW (3):** golden_set.json schema missing separate chapterId/sectionId fields, T062 mixes token/word units, no initial Render deployment task.

Coverage: 85 tasks covering ~97% of ~62 functional requirements. 0 orphaned tasks. 0 unresolved placeholders.

## Outcome

- ✅ Impact: 14 findings identified; 2 critical blockers before /sp.implement
- 🧪 Tests: N/A (read-only analysis)
- 📁 Files: No files modified
- 🔁 Next prompts: Resolve F1 (OpenAI Agents SDK decision) and F2 (move T070–T071 earlier) before /sp.implement; optionally run /sp.adr on the agent framework decision
- 🧠 Reflection: The OpenAI Agents SDK requirement in the constitution conflicts with the plan's direct httpx/OpenRouter integration — this is the highest-risk finding because it affects the architecture of 4 tasks and hackathon compliance

## Evaluation notes (flywheel)

- Failure modes observed: Prerequisites script does not support non-feature-branch workflows; worked around by reading files directly
- Graders run and results (PASS/FAIL): Not run
- Prompt variant (if applicable): n/a
- Next experiment: After resolving F1 and F2, re-run /sp.analyze to verify clean pass
