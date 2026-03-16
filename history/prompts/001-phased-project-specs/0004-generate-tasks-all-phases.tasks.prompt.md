---
id: "0004"
title: generate-tasks-all-phases
stage: tasks
date: 2026-03-13
surface: claude-code
model: claude-sonnet-4-6
feature: 001-phased-project-specs
branch: specification
user: metachemist
command: /sp.tasks
labels: [tasks, all-phases, rag, docusaurus, fastapi]
links:
  spec: specs/1-specify/spec.md
  ticket: ""
  adr: ""
  pr: ""
files:
  - path: specs/3-tasks/tasks.md
    action: created
tests:
  - n/a
---

## Prompt

/sp.tasks with user input:

"I'm using /sp.tasks to break my project into atomic work units.
Review my task list:
(1) Is each task atomic (does ONE thing with ONE acceptance criterion)?
(2) Are they sized right (15-30 minutes, not hours or minutes)?
(3) Can each be reviewed independently?
(4) Identify any tasks that should be split further or combined.
(5) Which tasks would you add or remove?"

Design artifacts read: specs/1-specify/spec.md (4-phase spec, 13 user stories), specs/2-plan/plan.md (FastAPI + Docusaurus + RAG pipeline), specs/2-plan/data-model.md (6 Postgres tables + Qdrant collection), specs/2-plan/contracts/openapi.yaml.

## Response snapshot

Generated specs/3-tasks/tasks.md with 85 tasks organized across 16 phases:

- Phase 1 (Setup): T001–T004 — directory structure, pyproject.toml, .gitignore, .env.example
- Phase 2 (Foundational): T005–T012 — config.py, db pool, alembic migration, main.py, CI/CD workflows
- Phases 3–5 (US1–US3): T013–T024 — Docusaurus scaffold, health endpoint, docker-compose, README
- Phase 6 (US4): T025–T039 — 13 chapter MDX files (T025–T037 all [P]), expert review, verification
- Phase 7 (US5): T040–T044 — chunker, embedder, ingestion service, ingest endpoint, run+verify
- Phase 8 (US6): T045–T051 — rag.py retrieval, db queries, rag.py streaming, chat endpoint, ChatPanel
- Phase 9 (US7): T052–T054 — SelectedTextBadge, wiring, backend selected-text handling
- Phase 10 (US8): T055–T060 — Better-Auth service, docker entry, auth middleware, profile endpoint, AuthModal, auth-guard UI
- Phases 11–13 (US9–US11): T061–T064 — agents.py router + 3 agent strategies
- Phases 14–15 (US12–US13): T065–T069 — personalize.py, translate.py, Urdu review
- Phase 16 (Polish/Demo): T070–T085 — golden set, benchmark, deployment verification, demo script, rehearsals, recording, submission

Atomicity applied: RAG service split into retrieval layer (T045) + streaming layer (T047) to keep each under 30 min. Chapter authoring split into 13 individual files. Agent strategies kept as separate tasks within shared file with coordination note.

## Outcome

- ✅ Impact: 85 atomic tasks generated covering all 4 project phases and 13 user stories; immediately executable by LLM or human developer
- 🧪 Tests: Not included (not requested in spec); golden eval set included as implementation tasks T070–T071
- 📁 Files: specs/3-tasks/tasks.md created
- 🔁 Next prompts: /sp.implement to begin executing tasks; /sp.analyze to cross-check tasks vs spec/plan
- 🧠 Reflection: The 13 parallel chapter-authoring tasks (T025–T037) are the largest single parallel block and represent the critical path into RAG functionality

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not run
- Prompt variant (if applicable): n/a
- Next experiment: Run /sp.analyze to verify task coverage against all spec FRs
