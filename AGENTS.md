# AGENTS.md

High-level operating guide for AI and human contributors in this repository.

## 1. Project Purpose

This repo defines and evolves an AI-native textbook for Physical AI and Humanoid Robotics, including architecture and quality standards for a RAG-enabled learning experience.

Primary goal: produce clear, accurate, implementation-ready documentation and supporting artifacts aligned with the project constitution.

## 2. Source-of-Truth Order

When instructions conflict, follow this order:

1. `constitution.md` (scope, governance, success criteria)
2. Inlined domain guide sections in `constitution.md` under `## Inlined Docs Archive`
3. `README.md` and `Quick-Start-Guide.md` (navigation and onboarding)

Do not introduce behavior, scope, or requirements that contradict the constitution.

## 3. Repository Reality

- This repository is currently documentation-first.
- `frontend/` and `backend/` exist but may be placeholders or partially implemented.
- Prefer improving and aligning docs unless the task explicitly requires implementation code.

## 4. How Agents Should Work

- Start by identifying the relevant guide section in `constitution.md` under `## Inlined Docs Archive`.
- Keep changes minimal, targeted, and consistent with existing structure.
- Preserve cross-references when moving or renaming sections/files.
- Favor concrete edits over broad rewrites.
- If a requirement is unclear, make the smallest safe assumption and state it.

## 5. Content and Style Expectations

- Keep language precise, instructional, and student-friendly.
- Maintain consistent terminology across files.
- Use progressive disclosure (simple to advanced).
- Prefer actionable examples over abstract statements.
- Follow markdown hierarchy and formatting conventions used in `constitution.md` process-related sections.

## 6. Quality Gates Before Finishing

Before completing a task, verify:

1. Internal links and references still resolve.
2. Claims and technical details are consistent with project docs.
3. Security and accessibility implications are addressed where relevant.
4. New content follows the QA checklist included in `constitution.md` (inlined archive).
5. Related docs were updated if the change affects shared assumptions.

## 7. Change Boundaries

- Do not add new frameworks, vendors, or major architectural decisions without explicit request.
- Do not fabricate benchmarks, test results, citations, or external approvals.
- Do not commit secrets, credentials, or environment-specific sensitive data.
- Do not delete or rewrite large sections of governance docs unless explicitly asked.

## 8. Preferred Contribution Pattern

1. Read the minimum required context.
2. Edit the smallest set of files needed.
3. Summarize exactly what changed and why.
4. Call out risks, assumptions, and follow-up actions.

## 9. Key Paths

- `constitution.md`
- `constitution.md#inlined-docs-archive`

## Active Technologies
- Python 3.11 (backend), Node.js 20 LTS (frontend) + FastAPI 0.111+, Uvicorn 0.30+, Docusaurus 3.x, qdrant-client 1.9+, asyncpg 0.29+, alembic 1.13+, python-dotenv (001-phased-project-specs)
- Neon Serverless Postgres (relational — users, sessions, messages schema), Qdrant Cloud Free Tier (vector store — single collection `physical_ai_textbook`) (001-phased-project-specs)

## Recent Changes
- 001-phased-project-specs: Added Python 3.11 (backend), Node.js 20 LTS (frontend) + FastAPI 0.111+, Uvicorn 0.30+, Docusaurus 3.x, qdrant-client 1.9+, asyncpg 0.29+, alembic 1.13+, python-dotenv
