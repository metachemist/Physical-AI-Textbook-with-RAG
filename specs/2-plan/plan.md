# Implementation Plan: Physical AI & Humanoid Robotics Textbook (All Phases)

**Branch**: `specification` | **Date**: 2026-03-13 | **Spec**: [spec.md](../1-specify/spec.md)

---

## Summary

Build an AI-native textbook for Physical AI and Humanoid Robotics — a Docusaurus static site with 13 week-chapters across 4 modules, backed by a FastAPI service that provides a RAG chatbot (grounded in book content), selected-text Q&A, optional auth, content personalization by learner track, Urdu translation, and three LLM subagents (quiz generator, chapter summarizer, prerequisite mapper).

Technical approach: Markdown-first content ingested via a two-pass chunker (`MarkdownHeaderTextSplitter` + `RecursiveCharacterTextSplitter` at 750 tokens / 100-token overlap), embedded locally with `sentence-transformers/all-MiniLM-L6-v2` (384d), stored in a single Qdrant collection with deterministic UUID5 point IDs, retrieved via two-prefetch RRF fusion, and streamed to the client through OpenRouter.

---

## Technical Context

**Language/Version**: Python 3.11 (backend), Node.js 20 LTS (frontend)
**Primary Dependencies**: FastAPI 0.111+, Uvicorn 0.30+, Docusaurus 3.x, qdrant-client 1.9+, asyncpg 0.29+, alembic 1.13+, sentence-transformers 2.x, langchain-text-splitters, tiktoken, python-frontmatter, python-dotenv, openai-agents (OpenAI Agents SDK)
**Storage**: Neon Serverless Postgres (users, sessions, messages, user_profiles), Qdrant Cloud Free Tier (collection: `physical_ai_textbook`, 384d COSINE)
**Testing**: pytest (backend unit + integration), Playwright or manual smoke (frontend)
**Target Platform**: Render free tier (backend API), GitHub Pages (Docusaurus frontend)
**Project Type**: Web application (backend + frontend)
**Performance Goals**: RAG response streaming starts ≤1s, completes ≤3s p95; health check ≤2s cold start; personalize/translation/agent endpoints ≤5s p95
**Constraints**: Free-tier services only; demo scale (1–10 concurrent users); no secrets in repository
**Scale/Scope**: 13 chapters, ~30 vector chunks total at launch, 1 Qdrant collection, 4 database tables

---

## Constitution Check

1. **Scope** — All phases align with constitution.md goals: textbook content, RAG interaction, optional personalization/translation/agents.
2. **Governance** — Phase gates are defined; no Phase N+1 work until Phase N exit criteria pass.
3. **Vendor lock-in** — All external services (OpenRouter, Qdrant, Neon, Render) are configurable via env vars; none require proprietary client SDKs not available via open-source alternatives.
4. **Secrets** — No credentials appear in source; `.env.example` documents every variable.
5. **Architecture** — No new frameworks or major vendors introduced beyond those in the constitution's technology list.

*Result: PASS. No violations requiring justification.*

---

## Project Structure

### Documentation (this feature)

```text
specs/
├── 1-specify/
│   └── spec.md              # Feature spec (all phases)
└── 2-plan/
    ├── plan.md              # This file
    ├── data-model.md        # Relational + vector schemas
    └── contracts/
        └── openapi.yaml     # Full API contract (Phase 1–3)
```

### Source Code (repository root)

```text
backend/
├── alembic/
│   ├── env.py
│   └── versions/
│       └── 001_initial_schema.py
├── app/
│   ├── main.py              # FastAPI app factory, lifespan, CORS
│   ├── config.py            # Pydantic Settings (reads .env)
│   ├── dependencies.py      # DB pool, Qdrant client, embedder as FastAPI deps
│   ├── api/
│   │   ├── health.py        # GET /health
│   │   ├── chat.py          # POST /api/v1/chat (RAG + SSE streaming)
│   │   ├── ingest.py        # POST /api/v1/ingest (admin, not in demo)
│   │   ├── personalize.py   # POST /api/v1/personalize
│   │   ├── translate.py     # POST /api/v1/translate
│   │   └── agents.py        # POST /api/v1/agents/{agentName}
│   ├── services/
│   │   ├── rag.py           # Retrieval + prompt assembly + OpenRouter call
│   │   ├── embedder.py      # sentence-transformers wrapper (local CPU)
│   │   ├── chunker.py       # Two-pass MDX chunker
│   │   └── ingestion.py     # Orchestrates chunker → embedder → Qdrant upsert
│   └── db/
│       ├── pool.py          # asyncpg connection pool
│       └── queries.py       # Typed query helpers (messages, user_profiles)
├── tests/
│   ├── unit/
│   │   ├── test_chunker.py
│   │   └── test_embedder.py
│   ├── integration/
│   │   └── test_health.py
│   └── golden/
│       ├── golden_set.json  # 30 questions, expected sections, difficulty
│       └── run_benchmark.py # Benchmark script: grounding, recall, hallucination
├── pyproject.toml
├── .env.example
└── Dockerfile               # Optional; Render uses native Python buildpack

auth/                            # Phase 3: Better-Auth microservice
├── index.ts                     # Express/Hono server (~50 lines)
├── package.json
└── Dockerfile

frontend/
├── docs/
│   ├── module-1-ros2/
│   │   ├── week-01-ros2-fundamentals.mdx
│   │   ├── week-02-ros2-advanced.mdx
│   │   ├── week-03-ros2-tooling.mdx
│   │   ├── week-04-ros2-navigation.mdx
│   │   └── week-05-ros2-capstone.mdx
│   ├── module-2-simulation/
│   │   ├── week-06-gazebo.mdx
│   │   └── week-07-unity.mdx
│   ├── module-3-nvidia-isaac/
│   │   ├── week-08-isaac-sim.mdx
│   │   ├── week-09-isaac-ros.mdx
│   │   └── week-10-isaac-perceptor.mdx
│   └── module-4-vla-humanoid/
│       ├── week-11-vla-foundations.mdx
│       ├── week-12-humanoid-platforms.mdx
│       └── week-13-deployment.mdx
├── src/
│   └── components/
│       ├── ChatPanel/
│       │   ├── index.tsx        # Chat panel with SSE streaming
│       │   ├── CitationLink.tsx
│       │   └── SelectedTextBadge.tsx
│       └── AuthModal/
│           └── index.tsx        # Phase 3: Better-Auth sign-up/in modal
├── docusaurus.config.ts
├── sidebars.ts
└── package.json
```

**Structure Decision**: Web application layout (Option 2). Backend and frontend are independent deployments (Render + GitHub Pages). No monorepo tooling required at demo scale.

---

## Parallel Work Tracks

Each phase has independent work tracks that can run concurrently. Sync points are where tracks must merge before downstream work can begin.

### Phase 1 — Three parallel tracks

```
Track A (Frontend Lead):      Docusaurus scaffold → sample chapter → GH Pages CI
Track B (Backend Lead):       FastAPI skeleton → health endpoint → Qdrant init → Alembic migration
Track C (Architecture Lead):  docker-compose.yaml → .env.example → README

                              ──── Sync: all three merge → verify SC-001 through SC-006 ────
```

### Phase 2 — Three parallel tracks, two sync points

```
Track A (AI Editor):     Author 13 chapter MDX files → Domain Expert review
Track B (Backend Lead):  Chunker → embedder → ingestion service → ingest endpoint
Track C (Frontend Lead): Chat panel UI → SSE consumer → selected-text detection → mobile responsive check

          ──── Sync 1: Track A content available → Track B ingestion runs ────
          ──── Sync 2: Track B RAG service ready → Track C integration test ────

Track D (AI Lead):       Golden eval set (can start once ~6 chapters published) → RAG benchmark
```

### Phase 3 — Two waves

```
Wave 1 (parallel, unblocks wave 2):
  Track A (Backend Lead):    Auth backend — Better-Auth setup → passthrough → middleware → profile endpoint
  Track B (Frontend Lead):   Auth UI — sign-up/in modal → protected button visibility

          ──── Sync: auth merged → protected features unblocked ────

Wave 2 (parallel):
  Track A (AI Lead):         Personalize endpoint + translate endpoint
  Track B (AI Lead):         Three agent implementations (quiz → summarizer → prerequisite)
  Track C (Frontend Lead):   Personalize button + translate button + revert control + agent UI triggers
```

### Phase 4 — Three parallel tracks

```
Track A (Demo Owner):        Demo script writing → 5 rehearsals → video recording
Track B (DevOps Owner):      Deployment verification → 3× health checks → rollback dry-run → procedure doc
Track C (Architecture Lead): Four fallback artifacts → static fallback page → README final update

          ──── Sync: all three merge → submission form completed ────
```

---

## Phase 1 — Setup & Infrastructure

### Entry / Exit Criteria

**Entry**: Repository exists with team write access; Qdrant Cloud + Neon Postgres free-tier accounts provisioned.

**Exit** (all required before Phase 2):
- SC-001 through SC-006 all pass
- At least one sample chapter stub visible at the published URL
- `GET /health` returns HTTP 200 with all sub-checks healthy from a cold start

### Design Decisions

| Concern | Decision | Rationale |
|---------|----------|-----------|
| Docusaurus version | 3.x with TypeScript config | LTS, best MDX 2 support |
| DB client | asyncpg (direct) + alembic | Lightest async PG driver; alembic handles schema migration |
| Migration strategy | `alembic upgrade head` as a docker-compose entrypoint command, before `uvicorn` starts | Separates migration runner from web process; avoids race conditions if multiple workers start; no programmatic alembic calls in app code. The docker-compose backend service runs: `alembic upgrade head && uvicorn app.main:app`. In production (Render), the build command runs `alembic upgrade head` and the start command runs `uvicorn`. |
| Qdrant collection creation | `collection_exists()` guard + `create_collection()` in lifespan | `qdrant-client 1.9` has no `if_not_exists` param; avoid `recreate_collection` (destructive) |
| Vector dimensions | 384 (all-MiniLM-L6-v2) | Fixed at collection creation; changing requires drop + recreate |
| Env validation | `pydantic-settings` with `BaseSettings` | Fails fast with a clear message listing missing keys |
| Single startup command | `docker compose up` | Spins both frontend (`npm run start`) and backend (`uvicorn`) with one command |
| CI | GitHub Actions: build frontend + link validation + `ruff` lint backend | Runs on every PR; target ≤4 min |

### Key Implementation Steps

| # | Step | Traces to |
|---|------|-----------|
| 1 | **Repository structure** — Create `backend/`, `frontend/`, top-level `docker-compose.yaml`, `.env.example` (all env vars documented with one-line descriptions), `README.md` with complete setup instructions reproducible on Ubuntu 22.04. | FR-011, FR-012, FR-014 |
| 2 | **Docusaurus scaffold** — `npx create-docusaurus@latest frontend classic --typescript`; configure `docusaurus.config.ts` with 4-module sidebar; add 1 sample chapter stub with proper heading hierarchy. | FR-001, FR-002 |
| 3 | **FastAPI skeleton** — `app/main.py` with lifespan that runs: env validation (fail-fast with descriptive error listing each missing var) → asyncpg pool init → Qdrant collection ensure. Alembic migration runs as an entrypoint command before uvicorn starts (not in the lifespan). | FR-005, FR-007, FR-008, FR-015 |
| 4 | **Health endpoint** — `GET /health` performs a `SELECT 1` on Postgres and a `get_collections()` on Qdrant; returns `{status, checks}` per OpenAPI contract. Non-200 with specific sub-check failure if any store is unreachable. | FR-006 |
| 5 | **Alembic migration 001** — Creates `users`, `accounts`, `sessions`, `verification`, `user_profiles`, `messages` tables. | FR-010 |
| 6 | **Qdrant collection init** — `collection_exists("physical_ai_textbook")` → create with `VectorParams(size=384, distance=Distance.COSINE)` → create payload indexes on `chapter_id`, `section_id`. Idempotent on subsequent runs. | FR-009 |
| 7 | **GitHub Pages deployment + link validation** — GitHub Actions workflow: `npm run build` → `lychee` or `docusaurus-plugin-broken-links` validates zero broken internal links → `peaceiris/actions-gh-pages` deploys. | FR-003, FR-004 |
| 8 | **CI pipeline** — GitHub Actions on every PR: build frontend + link validation + `ruff check` backend. Target ≤4 min. | FR-013 |
| 9 | **`docker-compose.yaml`** — `backend` service (Python 3.11, entrypoint: `alembic upgrade head && uvicorn app.main:app`, mounts `./backend`) + `frontend` service (Node 20, mounts `./frontend`); both read from `.env`. Phase 3 adds an `auth` service (Node 20, mounts `./auth`, port 3001). | FR-011 |

---

## Phase 2 — Base Features

### Entry / Exit Criteria

**Entry**: Phase 1 SC-001 through SC-006 all pass; published site URL stable and accessible; Qdrant collection and Neon schema confirmed accessible from the backend.

**Exit** (all required before Phase 3):
- SC-001 through SC-008 all pass
- The 30-question golden evaluation set is authored, reviewed, and stored in the repository
- RAG benchmark has been run at least once against the golden set with results documented

### Design Decisions

| Concern | Decision | Rationale |
|---------|----------|-----------|
| Chunking | `MarkdownHeaderTextSplitter` → `RecursiveCharacterTextSplitter` (tiktoken, 750t / 100t overlap) | Heading boundaries = natural semantic units for MDX; two-pass enforces token ceiling |
| MDX pre-processing | `python-frontmatter` strips YAML header; drop lines starting with `import ` | Prevents metadata noise in embeddings |
| Embedding | `sentence-transformers/all-MiniLM-L6-v2` local CPU | Zero cost, zero network dep, <30ms/batch, 384d |
| Point ID | `uuid.uuid5(NAMESPACE_URL, f"physical-ai-textbook:{chapter_id}:{chunk_index}")` | Deterministic, globally unique, stdlib-only; enables idempotent upsert |
| Upsert | `client.upsert(wait=True)` with `PointStruct` | Native insert-or-replace; `wait=True` ensures pipeline correctness |
| Retrieval boost | Two-prefetch `query_points()` + RRF fusion (chapter-scoped limit=5, global limit=10) | Works on Free Tier server version; simpler than score formula |
| Selected-text exact match | Embed selected text → inject matching chunk directly as primary context before retrieved results | Guarantees FR-015 (first paragraph addresses selected passage) |
| Fallback threshold | Cosine similarity < 0.70 → acknowledgment message, no LLM call | Prevents hallucination when no relevant content found |
| Streaming | SSE via `StreamingResponse` + `httpx.AsyncClient` streaming OpenRouter call | First token latency ≤1s target |
| LLM | OpenRouter `meta-llama/llama-3.1-8b-instruct:free`; model ID in env var | Swappable without code changes (FR-019) |
| Session context | Rolling last 5 exchanges fetched from `messages` table by `session_id` | Keeps prompt size bounded; no cross-session persistence |
| Code blocks | Docusaurus `@theme/CodeBlock` with built-in copy button | Native component; no custom implementation needed for FR-004 |
| Mobile responsive | Docusaurus default responsive layout; verify no horizontal scroll on 375px viewport | Satisfies FR-005 without custom CSS |

### Chapter Content Source

The 13 chapters are derived from the weekly breakdown in `Hackathon I_ Physical AI & Humanoid Robotics Textbook.md` and the module descriptions in `constitution.md`. The mapping:

| Chapter File | Week(s) | Topic | Key Concepts (from curriculum) |
|---|---|---|---|
| `week-01-ros2-fundamentals.mdx` | 1–2 | Introduction to Physical AI | Embodied intelligence, physical laws, humanoid robotics landscape, sensor systems (LiDAR, cameras, IMUs, force/torque) |
| `week-02-ros2-advanced.mdx` | 3 | ROS 2 Architecture | ROS 2 core concepts, nodes, topics, services, actions |
| `week-03-ros2-tooling.mdx` | 4 | ROS 2 Python Development | Building ROS 2 packages with Python (`rclpy`), launch files, parameter management |
| `week-04-ros2-navigation.mdx` | 5 | URDF and Robot Description | URDF format for humanoids, bridging Python agents to ROS controllers |
| `week-05-ros2-capstone.mdx` | 5 | ROS 2 Integration Capstone | ROS 2 package development project, end-to-end node communication |
| `week-06-gazebo.mdx` | 6 | Gazebo Simulation | Gazebo setup, URDF/SDF formats, physics simulation, sensor simulation |
| `week-07-unity.mdx` | 7 | Unity for Robotics | High-fidelity rendering, human-robot interaction, LiDAR/depth/IMU simulation |
| `week-08-isaac-sim.mdx` | 8 | NVIDIA Isaac Sim | Photorealistic simulation, synthetic data generation, Omniverse |
| `week-09-isaac-ros.mdx` | 9 | Isaac ROS | Hardware-accelerated VSLAM, visual SLAM, navigation |
| `week-10-isaac-perceptor.mdx` | 10 | Nav2 and Perception | Path planning for bipedal humanoids, AI-powered perception, sim-to-real |
| `week-11-vla-foundations.mdx` | 11 | Vision-Language-Action | VLA convergence, voice-to-action (Whisper), speech recognition |
| `week-12-humanoid-platforms.mdx` | 12 | Humanoid Development | Kinematics, dynamics, bipedal locomotion, manipulation, grasping |
| `week-13-deployment.mdx` | 13 | Capstone: Autonomous Humanoid | Cognitive planning (LLM → ROS 2 actions), multi-modal interaction, final project |

**Authoring prompt guidance**: Each chapter draft is generated by prompting the AI Editor with: the topic row above, the module description from the constitution, the learning outcomes from the Hackathon doc, and the structural requirements (≥800 words, learning objectives, ≥3 titled sections, ≥1 code example using `@theme/CodeBlock`, chapter summary). The Domain Expert review step focuses on technical accuracy of ROS 2 commands, API signatures, and simulation workflows.

### Chunk Payload Schema

```python
{
    "chapter_id":      "week-01-ros2-fundamentals",
    "module_id":       "module-1-ros2",
    "section_id":      "ros2-nodes-and-topics",
    "section_heading": "ROS 2 Nodes and Topics",
    "source_url":      "/docs/module-1-ros2/week-01-ros2-fundamentals#ros2-nodes-and-topics",
    "chunk_index":     3,
    "token_count":     712,
    "heading_level":   2,
    "text":            "..."   # stored for zero-I/O citation display
}
```

### RAG Pipeline (per request)

```
POST /api/v1/chat
  │
  ├─ Validate: message non-empty, ≤2000 chars
  │
  ├─ [selected_text present AND len ≥ 20?]
  │   ├── YES → embed selected_text → exact-match search → inject as primary chunk
  │   ├── NO (len < 20) → fall back to global retrieval; notify user selection too short (FR-016)
  │   └── NO (absent) → skip
  │
  ├─ Embed query (sentence-transformers, local)
  │
  ├─ Two-prefetch query_points():
  │   ├── Prefetch 1: filter(chapter_id == current), limit=5
  │   └── Prefetch 2: global, limit=10
  │   └── Fuse with RRF, return top 5
  │
  ├─ [top score < 0.70?]
  │   └── YES → return acknowledgment, no LLM call (FR-012)
  │
  ├─ Fetch rolling session context (last 5 exchanges from messages table) (FR-012a)
  │
  ├─ Assemble prompt: system + context chunks + session history + user question
  │
  ├─ Stream OpenRouter response via httpx.AsyncClient
  │
  ├─ SSE: yield delta events → yield final {answer, citations, latencyMs, done:true}
  │
  └─ Persist user message + assistant message to messages table (async, non-blocking)
```

### RAG Prompt Template

**Token budget** (for a ~4k context model like Llama 3.1 8B):
- System prompt: ~200 tokens (fixed)
- Retrieved chunks: ~3 chunks × 750 tokens = ~2,250 tokens (variable)
- Session history: last 3 exchanges × ~150 tokens = ~450 tokens (variable)
- User question: ~50 tokens
- Remaining for generation: ~1,050 tokens

**System prompt**:
```
You are a teaching assistant for the Physical AI & Humanoid Robotics textbook.
Answer the student's question using ONLY the provided context passages.

Rules:
1. Every factual claim must come from the context. Do not use your own knowledge.
2. If the context does not contain enough information to answer, say: "I couldn't find
   specific content on this topic in the textbook. Try rephrasing your question or
   asking about a related concept covered in the chapters."
3. Cite your sources using [Chapter: Section] format at the end of relevant sentences.
4. If the student highlighted text, address that passage directly in your first paragraph
   before expanding to related content.
5. Keep responses concise and student-friendly. Use examples from the context when available.
6. Do not mention that you are reading from "context passages" — respond naturally as if
   you know the textbook content.
```

**Context injection format** (per chunk):
```
--- Context from [{section_heading}] in [{chapter_id}] ---
{chunk_text}
Source: {source_url}
```

**Session history injection**: Prior exchanges are injected as alternating `User:` / `Assistant:` turns between the system prompt and the current question. Only the last 3 exchanges are included (not 5) when the model context window is ≤8k tokens to preserve chunk budget.

**Selected-text injection** (when present): The exact-match chunk is injected first with prefix `--- The student highlighted this passage ---` before the other retrieved chunks.

### Key Implementation Steps

| # | Step | Traces to |
|---|------|-----------|
| 1 | **Chapter content authoring** — Two-step pipeline: (a) AI Editor generates first drafts for all 13 MDX files from curriculum outline (≥800 prose words, learning objectives, ≥3 titled sections, ≥1 code example, chapter summary per chapter); (b) Domain Expert reviews each chapter for technical accuracy. A chapter MUST NOT be published until review is complete. Store in `frontend/docs/`. | FR-001, FR-002, FR-003 |
| 2 | **Code block copy-to-clipboard** — Use Docusaurus `@theme/CodeBlock` component which provides a built-in copy button. Verify all code examples in all 13 chapters use this component. | FR-004 |
| 3 | **Mobile responsiveness** — Verify the site renders without horizontal scroll on 375px viewport (mobile Chrome) and 1440px viewport (desktop Chrome). Test chapter navigation, chat panel, and code blocks on both. | FR-005, SC-007 |
| 4 | **Chunker service** (`services/chunker.py`) — Pre-process MDX (strip YAML frontmatter via `python-frontmatter`, drop JSX import lines) → `MarkdownHeaderTextSplitter` → `RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=750, chunk_overlap=100)` → return `(chunk_text, metadata)` tuples. Verify no chunk starts or ends mid-sentence. | FR-017 |
| 5 | **Embedder service** (`services/embedder.py`) — Load model once at startup; expose `embed_batch(texts) → List[List[float]]`. Model identifier read from `EMBEDDING_MODEL` env var; must be identical at ingestion and query time. | FR-019 |
| 6 | **Ingestion service** (`services/ingestion.py`) — Orchestrate chunker → embedder → UUID5 ID generation → `client.upsert(wait=True)`. Idempotent: re-running after chapter update replaces changed chunks without duplicates via `(chapter_id, chunk_index)` composite key. | FR-017, FR-018 |
| 7 | **Ingest endpoint** (`api/ingest.py`) — `POST /api/v1/ingest` admin-only trigger. Calls ingestion service for a single chapter. | FR-017 |
| 8 | **RAG service** (`services/rag.py`) — Embed query, run two-prefetch retrieval, check 0.70 threshold, fetch rolling session context (last 5 exchanges), build prompt, stream OpenRouter response. All claims grounded in retrieved chunks; no model-only knowledge. | FR-007, FR-008, FR-012, FR-012a, FR-014 |
| 9 | **Chat endpoint** (`api/chat.py`) — `POST /api/v1/chat`, validates request, enforces 60 req/min/IP rate limit via `slowapi`, calls RAG service, returns `StreamingResponse` (SSE). Error responses follow standard error model. | FR-007, FR-020, FR-022 |
| 10 | **Chat panel UI** (`src/components/ChatPanel/`) — Embedded in chapter pages (not separate page). States: idle → submitting → streaming → complete → error. Incremental display during streaming. Retry button in error state resubmits exact prior question. CORS restricted to deployed frontend origin. | FR-009, FR-010, FR-011, FR-021 |
| 11 | **Selected-text detection** — `useEffect` on `window.getSelection()`; display badge/indicator when selection ≥20 chars inviting user to ask about it. If selection < 20 chars and user submits, fall back to global retrieval and notify user the selection was too short. Pass `selectedText` in chat request. Clear selection returns to global retrieval mode. | FR-013, FR-014, FR-015, FR-016 |
| 12 | **Golden eval set** — 30 question/expected-answer pairs covering all 4 modules (minimum 6 per module). Mix of factual, conceptual, and troubleshooting prompts. Each includes the expected source section. Store in `backend/tests/golden/golden_set.json`. | FR-023 |
| 13 | **RAG benchmark** (`backend/tests/golden/run_benchmark.py`) — Two-phase benchmark. **Phase A (automated)**: Script runs all 30 questions via the chat endpoint and measures: (a) citation presence — response contains ≥1 citation (binary pass/fail per question); (b) Recall@10 — query the vector store directly, check if the expected source chunk (from golden set) appears in the top-10 results (target: ≥0.80 = SC-006). **Phase B (manual review with template)**: Script outputs a review spreadsheet (CSV) with columns: question, response, citations, expected section, and three blank label columns. A human reviewer labels each response: `grounded` (all claims traceable to retrieved chunks), `uncertain` (claim not directly contradicted but not sourced), or `hallucinated` (claim contradicts or goes beyond retrieved chunks). The same reviewer checks whether the first paragraph of selected-text responses directly references the selected passage. Targets: grounding 27/30 (SC-002), selected-text 27/30 (SC-004), hallucination ≤10% (SC-005). An LLM-as-judge step is NOT used — manual review is authoritative per spec. | SC-002, SC-004, SC-005, SC-006 |

---

## Phase 3 — Bonus Features

### Entry / Exit Criteria

**Entry**: Phase 2 SC-001 through SC-008 all pass; 30-question golden set complete and stored; RAG benchmark passed.

**Exit** (all required before Phase 4):
- SC-001 through SC-007 all pass for every bonus feature being shipped
- Any bonus feature not meeting its SC is formally cut and its UI entry point is hidden
- Auth-protected endpoints return HTTP 401 for unauthenticated requests, verified by automated test

### Implementation Order Justification

The spec's **priority order** is: Subagents → Better-Auth → Personalization → Urdu Translation.

The plan's **implementation order** places Auth first (steps 1–4) because auth is a runtime dependency for all other Phase 3 features: agents, personalization, and translation all require authentication. Building auth first unblocks parallel development of all three feature tracks. The subagent spec priority is preserved by completing agents before personalization and translation within Wave 2.

### Cut-Priority Table

Per spec: "Two bonuses executed excellently beats four bonuses executed poorly." If time pressure forces cuts:

| Priority | Feature | Cut if... | Minimum viable demo |
|----------|---------|-----------|---------------------|
| 1 (keep) | Auth + profile | Never — gates all other bonuses | Signup → signin → 401 for anonymous |
| 2 (keep) | Quiz generator agent | Never — highest-visibility agent, most self-contained | 5-question quiz on any chapter |
| 3 | Chapter summarizer agent | Not stable in rehearsal (>5s or hallucinated output) | Summary + 3 key points + citations |
| 4 | Personalization | Not stable in rehearsal or heading/code preservation fails | 1 section rewritten for software-engineer track |
| 5 | Prerequisite mapper agent | Time pressure | Concept list with source URLs |
| 6 | Urdu translation | No Urdu-proficient reviewer available for quality check | 1 section translated, formatting preserved |

Any cut feature has its UI entry point removed/disabled and is excluded from the demo script.

### Design Decisions

| Concern | Decision | Rationale |
|---------|----------|-----------|
| Auth library | Better-Auth (Node.js/TypeScript) running as a thin auth microservice | Spec mandates Better-Auth; it is a Node.js-only library with no Python SDK |
| Auth architecture | **Two-service pattern**: (1) A small Node.js service (~50 lines, Express or Hono) runs Better-Auth and handles `/api/auth/*` routes (signup, signin, signout, session). It connects to the shared Neon Postgres database and manages the `users`, `accounts`, `sessions`, `verification` tables. (2) FastAPI is the resource server — it validates session tokens by querying the `sessions` table directly (`SELECT * FROM sessions WHERE token = $1 AND expires_at > now()`). FastAPI never calls Better-Auth; it only reads the shared session state. | Better-Auth must run in a Node.js runtime. The shared-database pattern avoids HTTP round-trips between services for token validation. FastAPI treats the sessions table as a read-only auth contract. |
| Auth deployment | The auth service runs as a second container in docker-compose (`auth` service, Node 20, port 3001). On Render, it deploys as a second free-tier web service. The Docusaurus frontend calls `/api/auth/*` on the auth service URL directly (configured via env var `AUTH_SERVICE_URL`). | Keeps the auth service independent; FastAPI remains a pure Python service with no Node.js dependency. |
| Auth storage | `users`, `accounts`, `sessions`, `verification` tables (already in migration 001) | Schema pre-created in Phase 1; Better-Auth reads/writes these tables; FastAPI reads `sessions` for validation |
| Session TTL | 24 hours; token stored in `sessions` table with `expires_at` | User not required to re-authenticate within window (FR-009) |
| Sign-in errors | Generic message ("Invalid email or password") for all credential failures | Does not reveal whether email or password is wrong (FR-012) |
| Protected UI | Personalize/Translate/Quiz/Summarize/Prerequisite buttons hidden or disabled for unauthenticated users | Never sends request anonymously; shows "Sign in to use this feature" prompt (FR-011) |
| Track derivation | Priority-ordered rule table evaluated at read time; never stored | Tracks are derived, not stored, so profile changes take effect immediately |
| Default track | Beginner if profile is incomplete (unanswered questions) | Safe fallback; no degraded experience (FR-018) |
| Personalization scope | Session-scoped rewrite of section prose; headings and code blocks preserved exactly; inline replacement without page reload | Prevents structural drift; canonical content restored on refresh (FR-016, FR-017) |
| Translation | Preserve heading levels, bullet nesting, bold/italic, code fences; translate prose only; `formatPreserved` validated by structural comparison | Allows MDX renderer to handle translated output without modification |
| Revert control | UI toggle restores original English content client-side without page reload | Original markdown cached in React state before replacement (FR-022) |
| Urdu quality | Urdu-proficient reviewer evaluates at least 2 sample sections before feature is demo-ready | Required by FR-023; feature is cut if reviewer is unavailable |
| Agents | Single `POST /api/v1/agents/{agentName}` endpoint; each agent defined as an `Agent` instance via the OpenAI Agents SDK (`openai-agents`), with a custom model provider routing LLM calls through OpenRouter | Satisfies constitution's required stack (OpenAI Agents SDK); uniform contract; extensible without new routes |
| Agent grounding | All three agents use a Qdrant retrieval tool (registered via `@function_tool`) to fetch relevant chunks before the LLM generates output; same configurable model as RAG chatbot | Prevents model-only knowledge in agent output (FR-005); leverages SDK's built-in tool calling |

### Key Implementation Steps

**Wave 1: Auth (unblocks all other Phase 3 features)**

| # | Step | Traces to |
|---|------|-----------|
| 1 | **Better-Auth service** — Create `auth/` directory at repo root. Small Node.js service (~50 lines, Express or Hono) that runs Better-Auth with credential provider (email + password). Connects to the shared Neon Postgres database. Handles routes: `POST /api/auth/sign-up/email`, `POST /api/auth/sign-in/email`, `POST /api/auth/sign-out`, `GET /api/auth/session`. Session tokens stored in `sessions` table with 24h TTL. Sign-in errors are generic ("Invalid email or password"). Add `auth` service to docker-compose (Node 20, port 3001). Add `AUTH_SERVICE_URL` to `.env.example`. | P3 FR-006, FR-009, FR-012 |
| 2 | **Auth middleware in FastAPI** — FastAPI dependency that validates session tokens by querying the shared `sessions` table directly: `SELECT user_id FROM sessions WHERE token = $1 AND expires_at > now()`. Injects `current_user` or `None` (optional auth on chat, required on protected endpoints). Returns HTTP 401 with error code `AUTH_REQUIRED` for unauthenticated requests to protected endpoints. No HTTP calls to the auth service — reads shared database only. | P3 FR-010, FR-024 |
| 3 | **Auth service deployment** — Deploy the auth service as a second Render free-tier web service. Configure the frontend to call auth endpoints at `AUTH_SERVICE_URL` (env var). Verify signup/signin works E2E with the shared Neon database in the deployed environment. | P3 FR-006 |
| 4 | **User profile endpoint** — `POST /api/v1/profile` collects three questions during onboarding: Python level (beginner/intermediate/advanced), ROS experience (yes/no), AI knowledge (beginner/intermediate/advanced). `GET /api/v1/profile` returns stored profile + derived track via priority-ordered rules table. | P3 FR-007, FR-008 |
| 5 | **Auth UI** (`src/components/AuthModal/`) — Sign-up/sign-in modal with profile questionnaire on signup. Session token stored in `localStorage`. Bearer token attached to all authenticated requests. Protected UI buttons (Personalize, Translate, Quiz, Summarize, Prerequisite) hidden or disabled for unauthenticated users; shows "Sign in to use this feature" prompt instead. | P3 FR-006, FR-011 |

**Wave 2: Features (parallel after auth merges)**

| # | Step | Traces to |
|---|------|-----------|
| 6 | **Personalize endpoint** (`api/personalize.py`) — Requires auth. Load user profile → derive track (default to beginner if profile incomplete) → assemble system prompt with track-specific rewriting voice → call OpenRouter → **structural validation**: parse both original and rewritten markdown, extract heading nodes (text + level) and fenced code blocks (content + language tag); compare arrays for exact equality; if validation fails, return the original markdown with an error flag rather than serving broken output → return rewritten markdown + `appliedTrack`. Rate limit: 20 req/min per user. p95 latency target ≤5s. | P3 FR-013, FR-014, FR-015, FR-018, FR-026 |
| 7 | **Personalize UI** — "Personalize" button on each section. Replaces section content inline without page reload. Stores original markdown in React state for revert. Page refresh restores canonical content (session-scoped). | P3 FR-016, FR-017 |
| 8 | **Translate endpoint** (`api/translate.py`) — Requires auth. System prompt instructs model to translate prose only, preserve all heading levels, bullet nesting, bold/italic markers, and code fences. Code block content NOT translated. `formatPreserved` validated by comparing heading count, heading levels, and code fence count between source and output. Rate limit: 20 req/min per user. p95 latency target ≤5s. | P3 FR-019, FR-020, FR-021, FR-025 |
| 9 | **Translate UI** — "Translate → Urdu" button on each section. Replaces section inline. Revert control restores original English content client-side without page reload (original cached in React state). Anonymous users see "Sign in" prompt instead. | P3 FR-022, FR-011 |
| 10 | **Urdu quality review** — Urdu-proficient reviewer evaluates at least 2 translated sections for readability, accuracy, and structural preservation. Feature is cut if review is not completed. | P3 FR-023 |
| 11 | **Quiz generator agent** — Requires auth. Define `quiz_generator` as an `Agent` (OpenAI Agents SDK) with a `@function_tool` for Qdrant chunk retrieval by `chapter_id`. Custom model provider routes LLM calls through OpenRouter. Agent instructions: generate N MCQs at specified difficulty from retrieved chunks → return structured JSON with options, correct answer, explanation. Return graceful error if chapter has <500 words. Rate limit: 20 req/min. p95 ≤5s. | P3 FR-001, FR-004, FR-005, FR-025 |
| 12 | **Chapter summarizer agent** — Requires auth. Define `chapter_summarizer` as an `Agent` with same Qdrant retrieval tool. Retrieve all chapter chunks → prompt for summary + ≥3 key points adapted to proficiency level → return with citations. p95 ≤5s. | P3 FR-002, FR-005 |
| 13 | **Prerequisite mapper agent** — Requires auth. Define `prerequisite_mapper` as an `Agent` with same Qdrant retrieval tool. Retrieve topic chunks → prompt to identify prerequisite concepts → return structured list: each item has `concept` (str), `description` (str), `sourceUrl` (str). p95 ≤5s. | P3 FR-003, FR-005 |

---

## Phase 4 — Demo Video, Polish & Submission

### Entry / Exit Criteria

**Entry**: Phase 3 cut/keep decisions finalised; all features being shipped meet their Phase 3 exit criteria; demo environment running and reachable at stable URLs.

**Exit** (all required before submission):
- SC-001 through SC-008 all pass
- Submission form completed and confirmation receipt saved

### Design Decisions

| Concern | Decision | Rationale |
|---------|----------|-----------|
| Demo script | 5-segment timed walkthrough (0–15s, 15–35s, 35–55s, 55–70s, 70–90s) | Ensures all evaluation criteria demonstrated within 90s limit |
| Presenter constraints | Single narrator, max 2 visible browser tabs at any point | FR-017; reduces visual clutter for judges |
| Recording | Screen recording at 1080p+ with audio narration | FR-007; all on-screen text must be legible |
| Video hosting | YouTube unlisted or Loom — publicly accessible without auth | FR-008 |
| Rollback | Render's "Deploy a specific commit" via dashboard | FR-011; procedure documented, version-controlled, dry-run executed |
| Fallback strategy | Four pre-prepared artifacts covering the four most likely failure scenarios | FR-016; each verified in at least one rehearsal |
| Static fallback | Hosted page with architecture diagram, feature list, pre-recorded walkthrough clip | FR-013; last-resort if live deployment fails entirely |
| Submission | 4 artifacts: public GitHub repo URL, deployment URL, video link, WhatsApp number | FR-020 |

### Key Implementation Steps

**Deployment Hardening**

| # | Step | Traces to |
|---|------|-----------|
| 1 | **Frontend deployment verification** — Confirm GitHub Pages URL is stable and unchanged. Site loads within 3s, all chapter navigation works, zero console errors. | P4 FR-009 |
| 2 | **Backend deployment verification** — Confirm Render service URL is stable. Document service name and URL in README. | P4 FR-010 |
| 3 | **3× consecutive health checks** — Call `GET /health` at 1-minute intervals; all 3 return HTTP 200 with all sub-checks healthy. Save timestamped evidence (screenshots or curl output) before recording. | P4 FR-012, SC-003 |
| 4 | **Rollback procedure** — Write version-controlled procedure documenting exact steps for Render's "Deploy a specific commit" feature. Execute as a dry run: deploy a prior commit, verify health check passes, restore latest. Verify prior stable version restores within 5 minutes. | P4 FR-011, SC-004 |

**Polish**

| # | Step | Traces to |
|---|------|-----------|
| 5 | **Visual polish** — Fix any visual inconsistencies across chapters; verify mobile layout on 375px viewport; confirm zero broken links via CI. | P4 FR-009 |
| 6 | **End-to-end smoke test** — Run full golden set; verify 27/30 pass; record baseline metrics for grounding, recall, latency. | SC-002 through SC-006 from Phase 2 |
| 7 | **Feature freeze compliance** — No new features, schema changes, or dependency upgrades. Any unstable bonus feature has its UI entry point removed/disabled and is excluded from demo script. | P4 FR-021, FR-022, FR-023 |

**Demo Script & Rehearsal**

| # | Step | Traces to |
|---|------|-----------|
| 8 | **Written demo script** — Document narrator speech, user actions, and timing for all five segments: (a) 0–15s: homepage + module page + chapter navigation; (b) 15–35s: highlight text passage, submit question, chatbot streams response with citation; (c) 35–55s: bonus feature 1 (e.g. quiz agent); (d) 55–70s: bonus feature 2 (e.g. personalization); (e) 70–90s: show GitHub repo URL, architecture diagram, live app URL. Single narrator, max 2 browser tabs visible at any time. | P4 FR-014, FR-017 |
| 9 | **Four fallback artifacts** — Prepare and verify before recording: (a) Pre-loaded screenshot of a successful chat response with citations (for API unavailability); (b) Pre-authenticated backup browser tab with personalization or agent feature accessible (for auth failure); (c) Pre-generated translated section showing preserved Urdu formatting (for translation timeout); (d) Static fallback page at a known URL containing architecture diagram, feature list, and pre-recorded walkthrough clip (for full deployment failure). | P4 FR-013, FR-016, SC-006 |
| 10 | **5 rehearsals with timer** — Run demo script 5 times minimum. In at least 2 runs, inject a simulated failure and use the fallback. Target: at least 4 of 5 runs complete within 90 seconds. | P4 FR-015, SC-005 |

**Recording & Submission**

| # | Step | Traces to |
|---|------|-----------|
| 11 | **Screen recording** — Record at 1080p or higher with audio narration. Cover all 5 segments. All on-screen text legible. Verify total runtime ≤90 seconds via video editor timestamp before submission. | P4 FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007 |
| 12 | **Video hosting** — Upload to YouTube (unlisted) or Loom. Confirm publicly accessible without authentication. | P4 FR-008 |
| 13 | **Public repo verification** — Confirm GitHub repository is public. Open in incognito browser to verify full repo visible and clonable by anonymous reviewer. | P4 FR-018, SC-007 |
| 14 | **README final update** — Add live deployment URL, demo video link, architecture overview diagram, and feature checklist aligned to evaluation rubric. | P4 FR-019 |
| 15 | **Submission form** — Complete all four required fields: GitHub repo URL, deployment URL, demo video link, WhatsApp number. Save confirmation receipt (email or screenshot) as proof before deadline. | P4 FR-020, SC-008 |

---

## Cross-Cutting Concerns

### Environment Variables (`.env.example`)

```dotenv
# Neon Serverless Postgres
DATABASE_URL=postgresql+asyncpg://user:pass@host/db

# Qdrant Cloud
QDRANT_URL=https://<cluster-id>.cloud.qdrant.io
QDRANT_API_KEY=<key>
QDRANT_COLLECTION=physical_ai_textbook

# OpenRouter
OPENROUTER_API_KEY=<key>
LLM_MODEL=meta-llama/llama-3.1-8b-instruct:free

# Embedding (local; model name configures sentence-transformers load)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Better-Auth microservice (Phase 3)
BETTER_AUTH_SECRET=<secret>
AUTH_SERVICE_URL=http://localhost:3001

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://<github-pages-url>
```

### Rate Limits

| Endpoint | Limit | Enforced by |
|----------|-------|-------------|
| `POST /api/v1/chat` | 60 req/min per IP | `slowapi` FastAPI middleware |
| `POST /api/v1/personalize` | 20 req/min per user | `slowapi` + auth dependency |
| `POST /api/v1/translate` | 20 req/min per user | `slowapi` + auth dependency |
| `POST /api/v1/agents/*` | 20 req/min per user | `slowapi` + auth dependency |

### Error Handling

All endpoints return the `ErrorResponse` schema from the OpenAPI contract:
```json
{"apiVersion": "v1", "requestId": "req_xxx", "error": {"code": "...", "message": "..."}}
```

HTTP codes used: `422` validation, `401` auth required, `429` rate limited, `503` health degraded, `500` internal.

### Security Baseline

- All secrets via env vars; `.env` in `.gitignore`
- CORS restricted to `ALLOWED_ORIGINS` list
- No user-supplied content executed or reflected without sanitization
- SQL via asyncpg parameterized queries only (no string interpolation)
- Qdrant payload filters use typed `FieldCondition` (no raw string injection)
- Sign-in error messages generic (do not reveal email vs password)
