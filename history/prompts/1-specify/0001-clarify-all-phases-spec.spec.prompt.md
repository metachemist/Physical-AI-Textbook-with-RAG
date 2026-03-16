---
id: "0001"
title: clarify-all-phases-spec
stage: spec
date: 2026-03-13
surface: claude-code
model: claude-sonnet-4-6
feature: 1-specify
branch: 001-phased-project-specs
user: metachemist
command: /sp.clarify
labels: [clarification, rag, deployment, personalization, ingestion]
links:
  spec: specs/1-specify/spec.md
  ticket: ~
  adr: ~
  pr: ~
files:
  - specs/1-specify/spec.md
tests: ~
---

## Prompt

Run /sp.clarify on the combined all-phases spec at specs/1-specify/spec.md. Identify and resolve the top ambiguities across all 4 phases via interactive Q&A, then write each answer back into the spec.

## Response snapshot

5 questions asked and answered across the following categories:

1. **LLM provider** → OpenRouter (free-tier models, default `meta-llama/llama-3.1-8b-instruct:free`); written into Phase 2 FR-007 and Phase 3 FR-005.
2. **Profile-to-track mapping** → Priority-ordered rules table (ROS=yes → hardware/robotics; Python=advanced + AI≥intermediate → accelerated; Python≥intermediate → software engineer; default → beginner); written into Phase 3 FR-015 as an explicit table.
3. **Chunk identity key** → `(chapterId, chunkIndex)` composite key for upsert; written into Phase 2 FR-018 and Chunk entity definition.
4. **Relevance threshold** → Cosine similarity ≥ 0.70; written into Phase 2 FR-012.
5. **Backend deployment platform** → Render (free tier, dashboard rollback); written into Phase 4 FR-010, FR-011, and Assumptions.

## Outcome

- ✅ Impact: 5 previously ambiguous implementation decisions are now concrete, testable requirements in the spec.
- 🧪 Tests: Each clarification maps to at least one existing SC or acceptance scenario; no new SCs required.
- 📁 Files: specs/1-specify/spec.md (Clarifications section + Phase 2 FR-007, FR-012, FR-018, Phase 3 FR-005, FR-015, Phase 4 FR-010, FR-011, Assumptions)
- 🔁 Next prompts: /sp.plan — spec is now sufficiently clarified to begin implementation planning.
- 🧠 Reflection: The LLM provider and deployment platform questions had the highest downstream impact; resolving them early prevents architecture rework in planning.

## Evaluation notes (flywheel)

- Failure modes observed: Prerequisites script pointed to deleted spec path (specs/001-phased-project-specs/spec.md); resolved by using actual combined spec path directly.
- Graders run and results (PASS/FAIL): ~
- Prompt variant (if applicable): ~
- Next experiment (smallest change to try): Update .specify config or branch convention to point to specs/1-specify/ as the canonical feature directory.
