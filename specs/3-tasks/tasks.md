# Tasks: Physical AI & Humanoid Robotics Textbook (All Phases)

**Input**: Design documents from `specs/`
**Spec**: [specs/1-specify/spec.md](../1-specify/spec.md) | **Plan**: [specs/2-plan/plan.md](../2-plan/plan.md) | **Data Model**: [specs/2-plan/data-model.md](../2-plan/data-model.md)

**Organization**: Tasks are grouped by user story. Each phase produces an independently testable increment.
**Tests**: Not included (not requested in spec). Golden eval set included as implementation tasks (required by spec SC-002 through SC-006).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no blocking dependencies)
- **[US#]**: Which user story this task belongs to (see index below)
- Exact file paths included in all task descriptions

## User Story Index

| ID | Story | Project Phase | Priority |
|----|-------|--------------|----------|
| US1 | Student Opens the Textbook Site | Phase 1 | P1 |
| US2 | Developer Starts the Backend Service | Phase 1 | P1 |
| US3 | Developer Validates the Repository | Phase 1 | P2 |
| US4 | Student Reads the Textbook | Phase 2 | P1 |
| US5 | Chapter Content Is Indexed for Retrieval | Phase 2 | P2 |
| US6 | Student Asks the Chatbot a Question | Phase 2 | P1 |
| US7 | Student Asks About Selected Text | Phase 2 | P1 |
| US8 | User Signup and Signin | Phase 3 | P1 |
| US9 | Quiz Generator Agent | Phase 3 | P1 |
| US10 | Chapter Summarizer Agent | Phase 3 | P1 |
| US11 | Prerequisite Mapper Agent | Phase 3 | Bonus |
| US12 | Content Personalization | Phase 3 | P2 |
| US13 | Urdu Translation | Phase 3 | P2 |

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create the project skeleton — directory layout, dependency manifests, and git configuration. No feature code.

- [X] T001 Create top-level directory structure: `backend/app/api/`, `backend/app/services/`, `backend/app/db/`, `backend/alembic/versions/`, `backend/tests/golden/`, `frontend/`, `auth/`, `.github/workflows/`
- [X] T002 [P] Create `backend/pyproject.toml` with all Python dependencies: FastAPI 0.111+, uvicorn 0.30+, qdrant-client 1.9+, asyncpg 0.29+, alembic 1.13+, sentence-transformers 2.x, langchain-text-splitters, tiktoken, python-frontmatter, python-dotenv, slowapi, httpx, openai-agents (OpenAI Agents SDK), ruff
- [X] T003 [P] Create `.gitignore` with entries for `.env`, `__pycache__/`, `node_modules/`, `.venv/`, `*.pyc`, `dist/`, `.docusaurus/`
- [X] T004 [P] Create `backend/.env.example` documenting all env vars with one-line descriptions: `DATABASE_URL`, `QDRANT_URL`, `QDRANT_API_KEY`, `QDRANT_COLLECTION`, `OPENROUTER_API_KEY`, `LLM_MODEL`, `EMBEDDING_MODEL`, `BETTER_AUTH_SECRET`, `AUTH_SERVICE_URL`, `ALLOWED_ORIGINS`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core backend infrastructure every user story depends on — config, database pool, schema migration, FastAPI app factory, and CI.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [X] T005 Create `backend/app/config.py` with Pydantic `BaseSettings` reading `.env`; list all required keys; raise descriptive `ValueError` at startup naming each missing variable
- [X] T006 [P] Create `backend/app/db/pool.py` with `init_pool(dsn: str) → asyncpg.Pool` and `close_pool(pool)` for lifecycle management
- [X] T007 Create `backend/alembic/env.py` and `alembic.ini` configured to read `DATABASE_URL` from `backend/app/config.py` settings (not hardcoded)
- [X] T008 Create `backend/alembic/versions/001_initial_schema.py` with `upgrade()` creating all 6 tables per `specs/2-plan/data-model.md`: `users`, `accounts`, `sessions`, `verification`, `user_profiles`, `messages`
- [X] T009 Create `backend/app/main.py` with FastAPI app factory, CORS middleware reading `ALLOWED_ORIGINS`, slowapi `Limiter` registration, and `lifespan` context: env validation → asyncpg pool init → Qdrant collection ensure (`collection_exists` guard + `create_collection(VectorParams(size=384, distance=COSINE))` + payload indexes on `chapter_id` and `section_id`)
- [X] T010 Create `backend/app/dependencies.py` with `get_db_pool`, `get_qdrant_client`, and `get_embedder` as FastAPI `Depends`-compatible functions (embedder lazy-loaded once at startup)
- [X] T011 [P] Create `.github/workflows/ci.yml`: triggers on every PR; runs `npm run build` in `frontend/` and `ruff check backend/`; target runtime ≤4 min
- [X] T012 [P] Create `.github/workflows/pages.yml`: triggers on merge to `main`; builds Docusaurus with `npm run build`; runs internal link validation; deploys to GitHub Pages via `peaceiris/actions-gh-pages`

**Checkpoint**: Backend config, DB pool, Alembic, and CI ready — user story implementation can now begin

---

## Phase 3: User Story 1 — Student Opens the Textbook Site (Priority: P1) 🎯 MVP

**Goal**: Publish a navigable Docusaurus site at the GitHub Pages URL with module sidebar and sample chapter visible.

**Independent Test**: Open the published URL in Chrome; homepage loads < 3s, module sidebar renders with correct hierarchy, sample chapter page displays heading hierarchy, zero broken links reported by CI.

- [X] T013 [US1] Scaffold `frontend/` with Docusaurus 3.x TypeScript classic template: run `npx create-docusaurus@latest frontend classic --typescript` from repo root
- [X] T014 [US1] Configure `frontend/docusaurus.config.ts`: set `title`, GitHub Pages `url`/`baseUrl`/`organizationName`/`projectName`, and reference `sidebars.ts`
- [X] T015 [US1] Create `frontend/sidebars.ts` with 4-module hierarchy: `module-1-ros2` (5 chapters weeks 1–5), `module-2-simulation` (2 chapters weeks 6–7), `module-3-nvidia-isaac` (3 chapters weeks 8–10), `module-4-vla-humanoid` (3 chapters weeks 11–13)
- [X] T016 [US1] Create `frontend/docs/module-1-ros2/week-01-ros2-fundamentals.mdx` as a deployment-verification stub: outline headings + one introductory paragraph; all required heading slots present with placeholder text
- [X] T017 [US1] Verify GitHub Pages deployment: site accessible at published URL within 5 min of main branch merge; sample chapter renders in Chrome; zero broken links in CI run

**Checkpoint**: Textbook site live at GitHub Pages URL — US1 independently testable

---

## Phase 4: User Story 2 — Developer Starts the Backend Service (Priority: P1)

**Goal**: `GET /health` returns HTTP 200 with `database: ok` and `vectorStore: ok` from a cold start within 2 seconds.

**Independent Test**: Set valid env vars, run `docker compose up backend`, call `GET /health`; all three sub-checks show `ok` within 2 seconds; wrong `DATABASE_URL` returns HTTP 503 naming the failing sub-check.

- [X] T018 [US2] Create `backend/app/api/health.py` implementing `GET /health`: runs `SELECT 1` on asyncpg pool and `get_collections()` on Qdrant client; returns `{apiVersion, status, checks: {api, database, vectorStore}}` per `specs/2-plan/contracts/openapi.yaml`; returns HTTP 503 with specific failing sub-check name if either store is unreachable
- [X] T019 [US2] Register `/health` router in `backend/app/main.py` via `app.include_router(health.router)`
- [X] T020 [US2] Create `backend/app/db/queries.py` stub with module docstring and typed function signatures (no implementation yet; ready for Phase 8 body)
- [X] T021 [US2] Verify: start backend with valid `.env`, call `GET /health`, confirm HTTP 200 with all sub-checks `ok`; deliberately break `DATABASE_URL` and confirm HTTP 503 response names `database` as the failing check

**Checkpoint**: Backend starts and health check passes — US2 independently testable

---

## Phase 5: User Story 3 — Developer Validates the Repository (Priority: P2)

**Goal**: A developer clones the repo, follows the README on Ubuntu 22.04, and has both services running within 15 minutes with no undocumented steps.

**Independent Test**: Fresh clone, follow README only, run `docker compose up`; both frontend and backend start; no undocumented env vars or prerequisites.

- [X] T022 [P] [US3] Add backend service definition to `docker-compose.yaml`: Python 3.11 image, entrypoint `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000`, mounts `./backend`, reads from `.env`
- [X] T023 [P] [US3] Add frontend service definition to `docker-compose.yaml`: Node 20 image, command `npm run start`, mounts `./frontend`, port 3000
- [X] T024 [US3] Write `README.md` with complete Ubuntu 22.04 setup: prerequisites list, `cp .env.example .env` instruction with variable descriptions, `docker compose up` command, and service verification URLs (http://localhost:3000, http://localhost:8000/health)

**Checkpoint**: Single `docker compose up` starts both services — US3 independently testable

---

## Phase 6: User Story 4 — Student Reads the Textbook (Priority: P1)

**Goal**: All 13 week-chapters published with complete, expert-reviewed content (≥800 prose words, 3+ titled sections, ≥1 code example, chapter summary) across all 4 modules.

**Independent Test**: Open all 13 chapter URLs in Chrome; each has learning objectives, body sections with code examples using `@theme/CodeBlock`, and a summary; zero broken links in CI; no horizontal scroll on 375px mobile Chrome.

- [X] T025 [P] [US4] Author `frontend/docs/module-1-ros2/week-01-ros2-fundamentals.mdx`: Introduction to Physical AI — embodied intelligence, humanoid robotics landscape, sensor systems (LiDAR, cameras, IMUs, force/torque); ≥800 prose words; learning objectives; 3+ titled sections; `@theme/CodeBlock` example; chapter summary
- [X] T026 [P] [US4] Author `frontend/docs/module-1-ros2/week-02-ros2-advanced.mdx`: ROS 2 Architecture — nodes, topics, services, actions, DDS; ≥800 words; 3+ sections; code example
- [X] T027 [P] [US4] Author `frontend/docs/module-1-ros2/week-03-ros2-tooling.mdx`: ROS 2 Python Development — `rclpy`, building packages, launch files, parameter management; ≥800 words; 3+ sections; code example
- [X] T028 [P] [US4] Author `frontend/docs/module-1-ros2/week-04-ros2-navigation.mdx`: URDF for Humanoids — URDF/SDF joint types, bridging Python agents to ROS controllers; ≥800 words; 3+ sections; code example
- [X] T029 [P] [US4] Author `frontend/docs/module-1-ros2/week-05-ros2-capstone.mdx`: ROS 2 Integration Capstone — end-to-end package development, node communication project; ≥800 words; 3+ sections; code example
- [X] T030 [P] [US4] Author `frontend/docs/module-2-simulation/week-06-gazebo.mdx`: Gazebo Simulation — setup, URDF/SDF, physics simulation, sensor simulation; ≥800 words; 3+ sections; code example
- [X] T031 [P] [US4] Author `frontend/docs/module-2-simulation/week-07-unity.mdx`: Unity for Robotics — high-fidelity rendering, human-robot interaction, LiDAR/depth/IMU simulation; ≥800 words; 3+ sections; code example
- [X] T032 [P] [US4] Author `frontend/docs/module-3-nvidia-isaac/week-08-isaac-sim.mdx`: NVIDIA Isaac Sim — photorealistic simulation, synthetic data generation, Omniverse; ≥800 words; 3+ sections; code example
- [X] T033 [P] [US4] Author `frontend/docs/module-3-nvidia-isaac/week-09-isaac-ros.mdx`: Isaac ROS — hardware-accelerated VSLAM, visual SLAM, navigation; ≥800 words; 3+ sections; code example
- [X] T034 [P] [US4] Author `frontend/docs/module-3-nvidia-isaac/week-10-isaac-perceptor.mdx`: Nav2 and Perception — path planning for bipedal humanoids, AI perception stack, sim-to-real transfer; ≥800 words; 3+ sections; code example
- [X] T035 [P] [US4] Author `frontend/docs/module-4-vla-humanoid/week-11-vla-foundations.mdx`: Vision-Language-Action — VLA convergence, Whisper voice-to-action, speech recognition pipeline; ≥800 words; 3+ sections; code example
- [X] T036 [P] [US4] Author `frontend/docs/module-4-vla-humanoid/week-12-humanoid-platforms.mdx`: Humanoid Development — kinematics, dynamics, bipedal locomotion, manipulation and grasping; ≥800 words; 3+ sections; code example
- [X] T037 [P] [US4] Author `frontend/docs/module-4-vla-humanoid/week-13-deployment.mdx`: Capstone: Autonomous Humanoid — LLM → ROS 2 actions, multi-modal interaction, final project spec; ≥800 words; 3+ sections; code example
- [ ] T038 [US4] Domain Expert review of all 13 chapter MDX files: verify ROS 2 CLI commands, API signatures, and simulation workflow accuracy; commit corrections before any chapter is ingested or published
- [ ] T039 [US4] Verify all 13 chapters: ≥800 prose words each; CI link check passes with zero broken links; no horizontal scroll on 375px mobile Chrome; all `@theme/CodeBlock` examples render with copy button on 1440px desktop Chrome

**Checkpoint**: All 4 modules published with reviewed content — US4 independently testable

---

## Phase 7: User Story 5 — Content Indexed for Retrieval (Priority: P2)

**Goal**: All published chapter content chunked, embedded, and stored in Qdrant with correct chapter/section/source-URL metadata on every chunk.

**Independent Test**: Run ingestion pipeline against all 13 chapters; query Qdrant for 5 representative questions; confirm expected chapter sections appear in top-10 results for each query; re-run ingestion and confirm no duplicate chunks are created.

- [X] T040 [US5] Create `backend/app/services/chunker.py`: strip YAML frontmatter via `python-frontmatter`; drop lines starting with `import `; apply `MarkdownHeaderTextSplitter` then `RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=750, chunk_overlap=100)`; return `List[Tuple[str, dict]]` of (chunk_text, metadata); assert no chunk starts or ends mid-sentence
- [X] T041 [US5] Create `backend/app/services/embedder.py`: load `sentence-transformers/all-MiniLM-L6-v2` once at startup (model name from `EMBEDDING_MODEL` env var); expose `embed_batch(texts: List[str]) → List[List[float]]`; register as `get_embedder` FastAPI dependency
- [X] T042 [US5] Create `backend/app/services/ingestion.py`: orchestrate chunker → embedder → `uuid5(NAMESPACE_URL, f"physical-ai-textbook:{chapter_id}:{chunk_index}")` → `client.upsert(collection_name, wait=True, points=[PointStruct(...)])` with full payload schema from `specs/2-plan/data-model.md`; idempotent on re-run (upsert overwrites existing point at same ID)
- [X] T043 [US5] Create `backend/app/api/ingest.py` implementing `POST /api/v1/ingest`: accepts `{chapter_id, doc_path}`; calls `ingestion.run(chapter_id, doc_path)`; returns `{chunksUpserted: int, latencyMs: int}`; register router in `backend/app/main.py`
- [X] T044 [US5] Run ingestion pipeline against all 13 chapters; verify in Qdrant: ≥1 point per chapter; every point payload contains `chapter_id`, `section_id`, `source_url`, `text`; re-run and confirm point count is unchanged (idempotency check)

**Checkpoint**: All chapter content indexed in Qdrant — US5 testable; RAG chatbot (US6) can now start

---

## Phase 8: User Story 6 — Student Asks the Chatbot a Question (Priority: P1)

**Goal**: Anonymous user submits a question; receives a streaming grounded response with ≥1 citation within 3s; error state shows retry button.

**Independent Test**: Submit 30 golden questions via `POST /api/v1/chat`; ≥27 return grounded responses with ≥1 citation; p95 latency ≤3s; simulate network error; confirm retry button resubmits exact prior question.

- [X] T045 [US6] Create `backend/app/services/rag.py` retrieval layer: `embed_query(text, embedder) → vector`; run `client.query_points()` with two prefetches (chapter-scoped `limit=5` + global `limit=10`) fused with RRF; if top score < 0.70 return `{"fallback": True, "message": "I couldn't find specific content on this topic..."}` without making an LLM call
- [X] T046 [US6] Update `backend/app/db/queries.py` with `get_session_messages(pool, session_id, limit=10) → List[dict]` and `save_message(pool, session_id, user_id, chapter_id, role, content, citations)` using asyncpg parameterized queries (no string interpolation)
- [X] T047 [US6] Extend `backend/app/services/rag.py` with prompt assembly + streaming: fetch rolling context via `get_session_messages`; assemble system prompt + context chunks (format from `plan.md`) + session history + user question; stream via `httpx.AsyncClient` to OpenRouter (`LLM_MODEL` env var); yield SSE `data:` events → final event `{answer, citations, latencyMs, done: true}`
- [X] T048 [US6] Create `backend/app/api/chat.py` implementing `POST /api/v1/chat`: validate `message` non-empty and ≤2000 chars; apply `@limiter.limit("60/minute")` by IP; call `rag.stream_response(...)`; return `StreamingResponse(media_type="text/event-stream")`; persist both messages via `save_message` as a non-blocking background task
- [X] T049 [P] [US6] Create `frontend/src/components/ChatPanel/CitationLink.tsx`: render a `Citation` object as `<a href={sourceUrl} target="_blank">[{chapterId}: {sectionId}]</a>`
- [X] T050 [US6] Create `frontend/src/components/ChatPanel/index.tsx`: manage `ChatSession` state machine (idle → submitting → streaming → complete ↔ error); consume SSE with `EventSource`; display incremental text during streaming; render `CitationLink` list on completion; show retry button in error state that resubmits the exact prior question without modification
- [X] T051 [US6] Embed `ChatPanel` in Docusaurus chapter pages: add swizzle or MDX component to `frontend/docusaurus.config.ts` (or a theme component) so `<ChatPanel chapterId={...} />` appears at the bottom of every chapter page

**Checkpoint**: RAG chatbot functional end-to-end — US6 independently testable

---

## Phase 9: User Story 7 — Student Asks About Selected Text (Priority: P1)

**Goal**: Student highlights ≥20 chars; asks a question; first paragraph of response directly addresses the selected passage.

**Independent Test**: Highlight 30 passages across all modules; ask a question per passage; ≥27 responses reference the highlighted text in their first paragraph within 3s; highlight < 20 chars → submit → confirm fallback notice displayed.

- [X] T052 [P] [US7] Create `frontend/src/components/ChatPanel/SelectedTextBadge.tsx`: `useEffect` listening to `document.addEventListener("selectionchange")`; show badge when `window.getSelection().toString().length ≥ 20`; hide badge when selection clears or drops below 20 chars
- [X] T053 [US7] Wire `SelectedTextBadge` into `ChatPanel/index.tsx`: add `selectedText` to request body when badge is visible; after submit clear selection; when selection < 20 chars and user submits, display inline notice "Selection too short — searching all chapters instead"
- [X] T054 [US7] Update `backend/app/services/rag.py` to handle `selected_text` in request body: if present and `len ≥ 20`, embed the selected text → exact-match search → inject matching chunk as first context block with prefix `"--- The student highlighted this passage ---"`; if `len < 20`, skip selected-text path and set `noticeShort: true` in response metadata

**Checkpoint**: Selected-text Q&A functional — US7 independently testable

---

## Phase 10: User Story 8 — User Signup and Signin (Priority: P1)

**Goal**: Email+password signup with 3-question profile; 24h session; protected endpoints return HTTP 401 for anonymous requests.

**Independent Test**: Full signup → profile questionnaire → signout → signin flow completes 5 consecutive times; authenticated session persists across browser close/reopen within 24h; `POST /api/v1/agents/quiz_generator` without auth → HTTP 401 with `AUTH_REQUIRED`.

- [X] T055 [US8] Create `auth/package.json` with Better-Auth, Express (or Hono), and pg dependencies; create `auth/index.ts` (~50 lines) running Better-Auth credential provider connected to shared Neon Postgres, exposing: `POST /api/auth/sign-up/email`, `POST /api/auth/sign-in/email`, `POST /api/auth/sign-out`, `GET /api/auth/session`; all credential-failure responses return generic message "Invalid email or password"
- [X] T056 [US8] Add `auth` service to `docker-compose.yaml` (Node 20, port 3001, mounts `./auth`); add `BETTER_AUTH_SECRET` and `AUTH_SERVICE_URL` to `backend/.env.example` with one-line descriptions
- [X] T057 [US8] Create `backend/app/api/auth_middleware.py` with `get_current_user` FastAPI dependency: extract Bearer token from `Authorization` header; run `SELECT user_id FROM sessions WHERE token = $1 AND expires_at > now()` via asyncpg; return `user_id` UUID or raise `HTTPException(401, {"code": "AUTH_REQUIRED"})` for required-auth endpoints
- [X] T058 [US8] Create `backend/app/api/profile.py` implementing `POST /api/v1/profile` (requires auth: upsert `python_level`, `ros_experience`, `ai_knowledge` to `user_profiles`) and `GET /api/v1/profile` (returns stored profile + `derivedTrack` computed from priority-ordered rules table in `spec.md` FR-015)
- [X] T059 [US8] Create `frontend/src/components/AuthModal/index.tsx`: sign-up form with email + password + 3-question profile questionnaire (Python level, ROS experience, AI knowledge); sign-in form; on success store Bearer token in `localStorage`; attach `Authorization: Bearer <token>` header to all authenticated API requests
- [X] T060 [US8] Update `frontend` to auth-guard Personalize, Translate, Quiz, and Summarize buttons: if no token in `localStorage`, render "Sign in to use this feature" inline prompt instead of sending the request

**Checkpoint**: Auth flow complete — protected endpoints return 401 for anonymous; US8 independently testable

---

## Phase 11: User Story 9 — Quiz Generator Agent (Priority: P1)

**Goal**: Logged-in user requests a quiz on any chapter; receives N MCQs with options, correct answer, and explanation within 5s.

**Independent Test**: `POST /api/v1/agents/quiz_generator` with valid auth + `{chapterId, difficulty: "medium", count: 5}`; response contains exactly 5 questions each with 4 options, `correctAnswer`, `explanation`; same request without auth → HTTP 401.

- [X] T061 [US9] Create `backend/app/api/agents.py` implementing `POST /api/v1/agents/{agentName}` router: requires `get_current_user` dependency; applies `@limiter.limit("20/minute")` per user; dispatches to named `Agent` instance (OpenAI Agents SDK registry dict); returns `ErrorResponse(404)` for unknown `agentName`. Create a custom model provider class that routes LLM calls through OpenRouter using the `LLM_MODEL` env var. Define a shared `@function_tool` for Qdrant chunk retrieval by `chapter_id`. Register router in `backend/app/main.py`
- [X] T062 [US9] Implement `quiz_generator` as an `Agent` (OpenAI Agents SDK) in `backend/app/api/agents.py`: agent instructions specify MCQ generation grounded in retrieved chunks; uses shared Qdrant retrieval `@function_tool`; if retrieved content < 500 words return `ErrorResponse` with message "Insufficient content for a quiz on this section"; else generate `count` MCQs at `difficulty`; return `{questions: [{question, options: [str × 4], correctAnswer: str, explanation: str}]}`; p95 ≤5s

**Checkpoint**: Quiz Generator functional — US9 independently testable

---

## Phase 12: User Story 10 — Chapter Summarizer Agent (Priority: P1)

**Goal**: Logged-in user requests a chapter summary; receives summary paragraph + ≥3 key points + citations within 5s adapted to their proficiency level.

**Independent Test**: `POST /api/v1/agents/chapter_summarizer` with `{chapterId, proficiencyLevel: "beginner"}`; response has `summary` string, `keyPoints` array with ≥3 items, `citations` array; language accessible to beginner; same for `proficiencyLevel: "advanced"` and confirm different tone.

- [X] T063 [US10] Implement `chapter_summarizer` as an `Agent` (OpenAI Agents SDK) in `backend/app/api/agents.py`: uses shared Qdrant retrieval `@function_tool` to retrieve all chunks for `chapter_id`; agent instructions generate summary + ≥3 key points adapted to `proficiencyLevel`; return `{summary: str, keyPoints: str[], citations: Citation[]}`; p95 ≤5s

**Checkpoint**: Chapter Summarizer functional — US10 independently testable

---

## Phase 13: User Story 11 — Prerequisite Mapper Agent (Bonus)

**Goal**: Logged-in user submits a topic; receives a list of prerequisite concepts with recommended section source URLs.

**Independent Test**: `POST /api/v1/agents/prerequisite_mapper` with `{topic: "SLAM", chapterId: "week-09-isaac-ros"}`; response has `prerequisites` array with ≥2 items each containing `concept`, `description`, and `sourceUrl` pointing to a real chapter section.

- [X] T064 [US11] Implement `prerequisite_mapper` as an `Agent` (OpenAI Agents SDK) in `backend/app/api/agents.py`: uses shared Qdrant retrieval `@function_tool` to retrieve topic-relevant chunks; agent instructions identify prerequisite concepts with recommended section references; return `{prerequisites: [{concept: str, description: str, sourceUrl: str}]}` with ≥2 items when prerequisites exist; validate each `sourceUrl` points to a real chapter section slug; p95 ≤5s

**Checkpoint**: Prerequisite Mapper functional — US11 independently testable

---

## Phase 14: User Story 12 — Content Personalization (Priority: P2)

**Goal**: Logged-in user clicks Personalize on a section; prose rewritten to their derived track; headings and code blocks structurally identical to original.

**Independent Test**: Logged-in user with software-engineer track personalizes a section; prose uses API/integration analogies; `diff` of extracted heading nodes = empty; `diff` of extracted code blocks = empty; refresh restores canonical content.

- [X] T065 [US12] Create `backend/app/api/personalize.py` implementing `POST /api/v1/personalize` (requires auth): fetch user profile + derive track (beginner/software_engineer/hardware_robotics/accelerated per rules table FR-015); assemble track-specific system prompt; call OpenRouter; structural validation — extract heading nodes (text + level) and fenced code blocks from both original and rewritten; if arrays differ return original with `{validationFailed: true}` rather than broken output; apply `@limiter.limit("20/minute")` per user; p95 latency target ≤5s; return `{rewrittenMarkdown: str, appliedTrack: str}`
- [X] T066 [US12] Add "Personalize" button to `frontend` chapter section template: on click POST section markdown to `/api/v1/personalize`; replace prose inline; store original markdown in React state for revert; page refresh restores canonical content; unauthenticated users see "Sign in to use this feature"

**Checkpoint**: Personalization functional for all 4 tracks — US12 independently testable

---

## Phase 15: User Story 13 — Urdu Translation (Priority: P2)

**Goal**: Logged-in user clicks Translate → Urdu; prose replaced inline with Urdu; headings, code blocks, and markdown structure preserved exactly.

**Independent Test**: Translate a section; compare heading count + levels and code fence count between source and output — both must match; code block content not translated; Urdu reviewer confirms readability on ≥2 sections.

- [X] T067 [US13] Create `backend/app/api/translate.py` implementing `POST /api/v1/translate` (requires auth): system prompt instructs model to translate prose only, preserve all heading levels/bullet nesting/bold/italic/code fences; validate `formatPreserved` by comparing heading count + heading levels + code fence count between source and output; if validation fails return original with `{formatPreservedFailed: true}`; apply `@limiter.limit("20/minute")` per user; register router in `backend/app/main.py`
- [X] T068 [US13] Add "Translate → Urdu" button to `frontend` chapter section template: on click POST section markdown to `/api/v1/translate`; replace section inline; revert control restores original from React state without page reload; unauthenticated users see "Sign in to use this feature"
- [X] T069 [US13] Urdu quality review (manual): Urdu-proficient reviewer evaluates ≥2 translated sections for readability, accuracy, and structural preservation; document pass/fail findings in `specs/3-tasks/urdu-review.md`; feature is cut and UI button removed if review cannot be completed

**Checkpoint**: Urdu Translation functional and reviewer-approved — US13 independently testable

---

## Phase 16: Polish, Demo & Submission (Phase 4)

**Purpose**: Finalize deployment, build evaluation set, record demo, and submit.

- [X] T070 Create `backend/tests/golden/golden_set.json`: 30 questions covering all 4 modules (≥6 per module); mix of factual, conceptual, and troubleshooting prompts; each entry: `{question, expectedSection, module, difficulty}`
- [X] T071 Create `backend/tests/golden/run_benchmark.py`: Phase A — call `POST /api/v1/chat` for each golden question, record citation presence (pass/fail) and Recall@10 (expected section chunk in top-10 Qdrant results); Phase B — write CSV `{question, response, citations, expected_section, grounded, uncertain, hallucinated}` for manual grounding review
- [ ] T072 [P] Verify GitHub Pages deployment: all 13 chapter pages load < 3s; zero console errors; sidebar navigation complete; all code blocks render copy button
- [ ] T073 [P] Verify Render backend deployment: service URL stable; document service name and URL in `README.md`; run `docker compose up` locally to confirm single-command startup still works
- [ ] T074 Run 3× consecutive `GET /health` at 1-minute intervals; all 3 return HTTP 200 with all sub-checks `ok`; save timestamped curl output to `specs/3-tasks/health-check-evidence.txt`
- [X] T075 Write `backend/docs/rollback-procedure.md` documenting Render "Deploy a specific commit" steps; execute dry run (deploy prior commit → verify health passes → restore latest → verify health passes again); prior version must restore within 5 minutes
- [ ] T076 [P] Visual polish: fix any layout inconsistencies; verify 375px mobile viewport has no horizontal scroll; confirm CI link check passes with zero broken links
- [ ] T077 Run full 30-question golden benchmark via `run_benchmark.py`; verify ≥27/30 citation presence; calculate Recall@10 (target ≥0.80); record results in `specs/3-tasks/benchmark-results.md`
- [ ] T078 Feature freeze audit: for each bonus feature not meeting Phase 3 SC, hide/disable its UI entry point in `frontend/src/`; update demo script to skip it cleanly
- [X] T079 Write demo script covering 5 timed segments: (0–15s) homepage + module + chapter nav; (15–35s) highlight text → chatbot streams → citation displayed; (35–55s) quiz agent; (55–70s) personalization; (70–90s) GitHub URL + architecture diagram + live app URL; single narrator, max 2 browser tabs visible
- [X] T080 Prepare 4 fallback artifacts: (a) screenshot of successful chat response with citations; (b) pre-authenticated backup browser tab; (c) screenshot of Urdu section with preserved formatting; (d) static fallback page with architecture diagram + feature list + pre-recorded clip at known URL
- [ ] T081 Run 5 rehearsals with timer; inject simulated failure in ≥2 rehearsals and use fallback; target ≥4 of 5 runs complete within 90 seconds
- [ ] T082 Record demo at 1080p+ with audio narration; verify runtime ≤90s via video editor timestamp; all 5 segments and all on-screen text legible
- [ ] T083 [P] Upload demo video to YouTube (unlisted) or Loom; confirm publicly accessible in incognito browser without authentication
- [ ] T084 [P] Verify GitHub repo is public in incognito browser; update `README.md` with live deployment URL, demo video link, architecture diagram, and evaluation rubric feature checklist
- [ ] T085 Complete submission form: GitHub repo URL, Render deployment URL, demo video link, WhatsApp number; save confirmation receipt (email or screenshot) before deadline

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 completion
- **US1, US2, US3 (Phases 3–5)**: All depend on Foundational — can run in parallel after Phase 2
- **US4 (Phase 6)**: Depends on US1 (Docusaurus scaffold); 13 chapters can be authored in parallel
- **US5 (Phase 7)**: Depends on US4 (chapters authored) and US2 (Qdrant initialized)
- **US6 (Phase 8)**: Depends on US5 (content indexed) and Foundational (DB queries ready)
- **US7 (Phase 9)**: Depends on US6 (ChatPanel must exist)
- **US8 (Phase 10)**: Can start after Foundational — runs in parallel with US4–US7
- **US9, US10, US11 (Phases 11–13)**: Depend on US8 (auth required); agent strategies can be added in parallel
- **US12, US13 (Phases 14–15)**: Depend on US8 (auth required); run in parallel with each other
- **Phase 16**: Depends on all desired user stories complete

### User Story Dependency Graph

```
Foundational (Phase 2)
    ├── US1 (Docusaurus site)
    │   └── US4 (Chapter content — 13 parallel tasks)
    │       └── US5 (Content ingestion)
    │           └── US6 (RAG chatbot)
    │               └── US7 (Selected-text Q&A)
    ├── US2 (Backend health)
    ├── US3 (Repo / docker-compose)
    └── US8 (Auth) ──────────────────── Wave 2 (all parallel):
            ├── US9  (Quiz Generator)
            ├── US10 (Chapter Summarizer)
            ├── US11 (Prerequisite Mapper)
            ├── US12 (Personalization)
            └── US13 (Urdu Translation)
```

### Parallel Opportunities

- **Phase 1**: T002, T003, T004 can run in parallel (different files)
- **Phase 2**: T011, T012 (CI workflows) can run in parallel
- **Phases 3–5**: US1, US2, US3 can all start at the same time after Foundational
- **Phase 6**: T025–T037 (13 chapter files) all run in parallel — largest parallel block in the project
- **Phase 8**: T049 (CitationLink.tsx) runs parallel with T050 (ChatPanel/index.tsx)
- **Phase 9**: T052 (SelectedTextBadge) runs parallel with T053–T054 (wiring + backend)
- **Phase 10 → Wave 2**: Once US8 merges, US9–US13 all start in parallel
- **Phase 16**: T072, T073, T076, T083, T084 run in parallel

---

## Parallel Example: Phase 6 (Chapter Authoring — 13 files)

```bash
# All 13 chapter files can be authored simultaneously (independent files):
Task T025: frontend/docs/module-1-ros2/week-01-ros2-fundamentals.mdx
Task T026: frontend/docs/module-1-ros2/week-02-ros2-advanced.mdx
Task T027: frontend/docs/module-1-ros2/week-03-ros2-tooling.mdx
Task T028: frontend/docs/module-1-ros2/week-04-ros2-navigation.mdx
Task T029: frontend/docs/module-1-ros2/week-05-ros2-capstone.mdx
Task T030: frontend/docs/module-2-simulation/week-06-gazebo.mdx
# ... T031–T037
# Then T038 (domain expert review) blocks T039 (verification)
```

## Parallel Example: Wave 2 (Auth-gated bonus features)

```bash
# After T060 (auth UI complete), these 5 stories start in parallel:
Task T062: QuizGeneratorAgent strategy in backend/app/api/agents.py
Task T063: ChapterSummarizerAgent strategy in backend/app/api/agents.py   # coordinate: same file
Task T064: PrerequisiteMapperAgent strategy in backend/app/api/agents.py  # coordinate: same file
Task T065: backend/app/api/personalize.py (separate file — fully parallel)
Task T067: backend/app/api/translate.py   (separate file — fully parallel)
```

---

## Implementation Strategy

### MVP First: Phase 1 + Phase 2 User Stories (US1–US7)

1. Complete Phase 1: Setup (T001–T004)
2. Complete Phase 2: Foundational (T005–T012)
3. US1 — Textbook site live (T013–T017)
4. US2 — Backend health passing (T018–T021)
5. US3 — Single `docker compose up` works (T022–T024)
6. US4 — All 13 chapters published, expert-reviewed (T025–T039, parallel authoring)
7. US5 — All chapters indexed in Qdrant (T040–T044)
8. US6 — RAG chatbot streaming with citations (T045–T051)
9. US7 — Selected-text Q&A working (T052–T054)
10. **STOP AND VALIDATE**: Run golden set benchmark (T071); verify SC-001 through SC-008 pass

### Incremental Delivery

- After MVP: add auth (US8) → unlocks all Phase 3 features
- Add agents (US9, US10, US11) in parallel
- Add personalization (US12) + translation (US13) in parallel
- Each bonus adds demonstrable value without breaking Phase 2 features

---

## Notes

- [P] tasks involve different files with no cross-dependencies — safe to run in parallel without coordination
- Content authoring tasks (T025–T037) are designed for an AI Editor first-draft pass; T038 (domain expert review) MUST complete before T044 (ingestion run)
- T061–T064 (agent strategies) all modify `agents.py` — coordinate to avoid merge conflicts when implementing multiple strategies concurrently
- T075 (rollback procedure) must be executed as a live dry run, not just written as documentation
- T081 (demo rehearsals) is a hard gate: any bonus feature that fails ≥2 of 5 runs is cut per spec Phase 3 cut-priority table
- Total tasks: 85 | Phase 1: 4 | Phase 2: 8 | US1–US3: 12 | US4: 15 | US5: 5 | US6: 7 | US7: 3 | US8: 6 | US9–US11: 4 | US12–US13: 5 | Phase 16: 16
