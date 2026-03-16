---
id: "0002"
title: clarify-4-phase-specs-ambiguities
stage: spec
date: 2026-03-13
surface: claude-code
model: claude-sonnet-4-6
feature: 001-phased-project-specs
branch: 001-phased-project-specs
user: metachemist
command: /sp.clarify
labels: [clarify, ambiguity, terminology, architecture]
links:
  spec: specs/1-specify/phase-02/spec.md
  ticket: ""
  adr: ""
  pr: ""
files:
  - specs/1-specify/phase-01/spec.md
  - specs/1-specify/phase-02/spec.md
  - specs/1-specify/phase-03/spec.md
  - specs/1-specify/phase-04/spec.md
tests: []
---

## Prompt

Analyze all specs in the specs/1-specify folder for: (1) ambiguous terms, (2) missing assumptions, (3) incomplete requirements, (4) scope conflicts. What gaps should be addressed before planning?

## Response snapshot

5 questions asked and answered across a sequential clarification loop. All four phase specs updated incrementally after each accepted answer.

Q1 — Content hierarchy: Module/Chapter/Section were used interchangeably across all phases. → B: Three levels — Module (4 total) → Chapter (one per week, ~13 total) → Section (H2/H3 headings). Updated Phase 2 FR-001, Key Entities (added Module and Section as distinct entities), acceptance scenario wording, and Phase 1 sidebar nav description. Clarifications block added to all four specs.

Q2 — Within-session chat memory: Phase 2 Non-Goals ruled out cross-session persistence but was silent on within-session. → B: Rolling window of last 3–5 exchanges per session. Added FR-012a, updated Non-Goals wording, added acceptance scenario 5 to User Story 2, updated Chat Exchange entity with window size.

Q3 — "Grounded" definition: Used 12+ times as a quality term but never formally defined; two reviewers could score the same response differently. → B: Every factual claim traceable to a retrieved chunk; no model-only knowledge. Defined in FR-007, applied to SC-002 and SC-005 (expanded to 3-label rubric: grounded/uncertain/hallucinated), updated Phase 3 FR-005.

Q4 — Chapter authoring process: Ownership said "Author + AI Editor" but didn't define who produces the first draft or how. → B: Claude Code generates first draft from curriculum outline; Domain Expert reviews for technical accuracy. Updated Phase 2 ownership table, FR-003 (two-step pipeline), and Assumptions (Domain Expert availability constraint added).

Q5 — Concurrent user scale: No target defined anywhere; affects infrastructure sizing, rate limit calibration, and free-tier adequacy. → A: Demo scale, 1–10 concurrent users. Added FR-023a (explicit scale boundary and free-tier adequacy statement), updated Phase 1 and Phase 2 Assumptions, anchored Phase 4 deployment stability definition to demo scale.

## Outcome

- ✅ Impact: 5 critical ambiguities resolved; all four phase specs are unambiguous enough to proceed to /sp.plan
- 🧪 Tests: SC-005 now has a 3-label scoring rubric; FR-012a (rolling memory) is independently testable; FR-023a sets a hard concurrent-user boundary
- 📁 Files: 4 phase specs updated with Clarifications blocks and targeted changes to FRs, SCs, Entities, Assumptions, and Ownership
- 🔁 Next prompts: /sp.plan phase-01
- 🧠 Reflection: Content hierarchy (Q1) and grounded definition (Q3) were the two highest-leverage clarifications — both propagated across multiple FRs and SCs in multiple phases

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All 5 questions answered and applied; no contradictory statements remain
- Prompt variant (if applicable): ""
- Next experiment: Run /sp.plan on phase-01 to verify that clarified specs produce unambiguous task decomposition without further clarification loops
