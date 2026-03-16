# Feature Specification: Physical AI & Humanoid Robotics Textbook (All Phases)

**Feature Branch**: `chore/setup-spec-architecture`
**Created**: 2026-03-13
**Status**: Draft
**Phases**: 1 through 4

---

## Phase Index

| Phase | Title |
|-------|-------|
| [Phase 1](#phase-1--setup--infrastructure) | Setup & Infrastructure |
| [Phase 2](#phase-2--base-features) | Base Features (Book + RAG + Selected-Text Q&A) |
| [Phase 3](#phase-3--bonus-features) | Bonus Features (Subagents, Auth, Personalization, Urdu) |
| [Phase 4](#phase-4--demo-video-polish--submission) | Demo Video, Polish & Submission |

---

## Shared Clarifications

The following clarifications apply to all phases.

- **Content hierarchy**: Three levels: Module (4 total) → Chapter (~13 total, one per curriculum week) → Section (H2/H3 headings within a chapter).
- **Session memory**: Rolling window — the last 5 exchanges are included as context in every request within the same browser session (reduced to 3 when the model context window is ≤8k tokens to preserve chunk budget). History does not persist across sessions.
- **Grounded definition**: Every factual claim in the response is traceable to a chunk returned by the vector store for that request. No assertion is made from model-only knowledge. A response that contains a citation but asserts additional facts not present in any retrieved chunk is NOT grounded.
- **Peak concurrent users**: Demo scale — 1–10 concurrent users (judges and presenter). Free-tier services are sufficient and rate limits are calibrated for this load. The system is not designed for classroom or public scale.

---

## Clarifications

### Session 2026-03-13

- Q: Which LLM service powers RAG responses and agent features? → A: OpenRouter (multi-model gateway), targeting free-tier models (e.g., `meta-llama/llama-3.1-8b-instruct:free`) for the demo; model can be swapped via configuration without code changes.
- Q: How should the 3 profile answers determine the active personalization track? → A: A rules table maps answer combinations to a track using a priority-ordered lookup (evaluated top-to-bottom, first match wins).
- Q: What uniquely identifies a chunk for idempotent ingestion? → A: `(chapterId, chunkIndex)` composite key — the pipeline overwrites the vector at this position on every re-run.
- Q: What cosine similarity threshold triggers the "no relevant results" fallback? → A: `0.70` — if the highest-scoring retrieved chunk scores below 0.70, the system MUST respond with the explicit acknowledgment rather than generating a grounded response.
- Q: Which platform will host the FastAPI backend? → A: Render (free tier, auto-deploy from GitHub, dashboard-based rollback).

---

## Phase 1 — Setup & Infrastructure


### Overview

Establish the complete project foundation: repository layout, published textbook site scaffold, backend service skeleton, and validated connections to the vector store and relational database. This phase is a hard gate — no Phase 2 work begins until all Phase 1 exit criteria pass.

---

### Non-Goals

The following are explicitly out of scope for Phase 1:

- Any application feature code (RAG, chatbot, personalization, translation, auth)
- Multi-environment setup (dev/staging/prod separation)
- Production-grade CI (integration tests, coverage gates, security scans)
- Full chapter content — the sample chapter is a stub (outline + one intro paragraph only)
- Backend authentication or session management
- Content ingestion or vector embedding

---

### Phase 1 Gates

**Entry criteria** (before Phase 1 work begins):
- Repository exists and the team has write access
- Qdrant Cloud account and Neon Postgres account are provisioned (free tier)

**Exit criteria** (all must pass before Phase 2 begins):
- SC-001 through SC-006 all pass
- At least one sample chapter stub is visible at the published URL
- `GET /health` returns HTTP 200 with all sub-checks healthy from a cold start

---

### Phase 1 Ownership

| Deliverable | Owner Role |
|-------------|------------|
| Repository structure and README | Architecture Lead |
| Docusaurus site scaffold and GitHub Pages deployment | Frontend Lead |
| FastAPI service skeleton and health endpoint | Backend Lead |
| Qdrant collection schema definition | Backend Lead |
| Neon Postgres schema migration | Backend Lead |
| CI pipeline | DevOps Owner |
| `.env.example` and local startup command | Architecture Lead |

---

### Phase 1 User Scenarios & Testing

#### User Story 1 — Student Opens the Textbook Site (Priority: P1)

A student navigates to the published URL and sees a working textbook homepage with chapter navigation and at least one sample chapter visible.

**Why this priority**: Without a published, navigable site there is nothing to evaluate Phase 2 content work has no deployment target.

**Independent Test**: Deploy the site and confirm the homepage loads, chapter sidebar appears, and one sample chapter page renders without broken links in Chrome.

**Acceptance Scenarios**:

1. **Given** the site build completes without errors, **When** the published URL is opened in Chrome, **Then** the homepage loads within 3 seconds with no console errors.
2. **Given** chapter navigation links are present in the sidebar, **When** a student clicks a chapter link, **Then** the correct chapter page renders with proper heading hierarchy.
3. **Given** the site is built from source, **When** the internal link checker runs, **Then** zero broken internal links are reported.

---

#### User Story 2 — Developer Starts the Backend Service (Priority: P1)

A developer runs a single command to start the backend service, calls the health endpoint, and receives confirmation that the API, database, and vector store are all reachable.

**Why this priority**: The RAG chatbot and all bonus features depend on the backend being runnable and connected to its data stores before any feature code is written.

**Independent Test**: Run the local startup command, then call the health endpoint; it returns HTTP 200 with all sub-checks passing.

**Acceptance Scenarios**:

1. **Given** valid environment variables are set, **When** the backend service starts, **Then** the health endpoint returns HTTP 200 confirming the API, database, and vector store are all reachable.
2. **Given** the database connection string is correct, **When** the health check runs, **Then** a connectivity test completes without error.
3. **Given** the vector store credentials are correct, **When** the health check runs, **Then** the collection listing call succeeds.

---

#### User Story 3 — Developer Validates the Repository (Priority: P2)

A developer clones the repository, reads the README, and can reproduce the full local setup without asking questions.

**Why this priority**: A clear, reproducible structure demonstrates project quality.

**Independent Test**: A second developer follows the README from a fresh clone and has both frontend and backend running within 15 minutes with no undocumented steps.

**Acceptance Scenarios**:

1. **Given** the README contains setup steps, **When** a developer follows them on Ubuntu 22.04, **Then** both the frontend and backend start successfully.
2. **Given** the repository layout matches the constitution, **When** a reviewer inspects the top-level directories, **Then** all required directories and files are present as specified in the constitution.

---

#### Phase 1 Edge Cases

- What happens when environment variables are missing at startup? The service fails fast with a descriptive error listing each missing variable by name.
- What happens when the vector store or database is temporarily unreachable? The health endpoint returns a non-200 status identifying the specific failing sub-check; the process does not crash silently.
- What happens when the site build encounters a malformed content file? The build fails with a clear error pointing to the offending file rather than silently producing a broken page.

---

### Phase 1 Requirements

#### Functional Requirements

**Textbook Site**

- **FR-001**: The system MUST provide a working textbook site built with Docusaurus that builds without errors and produces a deployable static output.
- **FR-002**: The site MUST include a homepage, chapter sidebar navigation, and at least one complete sample chapter stub with proper heading hierarchy.
- **FR-003**: The site MUST be automatically deployed to GitHub Pages whenever changes are merged to the main branch, with no manual deployment step required.
- **FR-004**: The site MUST pass internal link validation with zero broken links before every deployment.

**Backend Service**

- **FR-005**: The system MUST provide a backend service built with FastAPI that starts from a single command and exposes a health check endpoint.
- **FR-006**: The health check endpoint MUST report the individual status of the API process, the relational database connection, and the vector store connection.
- **FR-007**: The backend MUST connect to Neon Serverless Postgres and validate the connection is live on every startup.
- **FR-008**: The backend MUST connect to Qdrant Cloud and validate that the designated collection is accessible on every startup.
- **FR-009**: If the collection does not exist, the backend MUST create it with the correct schema on first run, and the creation MUST be idempotent on subsequent runs.
- **FR-010**: The relational database schema (users, sessions, messages tables as defined in the constitution) MUST be applied automatically via migration on startup.

**Developer Experience**

- **FR-011**: The system MUST provide a single command that starts both the frontend and backend locally for development.
- **FR-012**: The system MUST provide an `.env.example` file documenting every required environment variable with a one-line description of its purpose.
- **FR-013**: A CI pipeline MUST run on every pull request and verify at minimum: the site builds without errors and the backend has no import or lint errors.
- **FR-014**: The README MUST contain complete setup instructions reproducible on Ubuntu 22.04 from a fresh clone, covering environment variable setup, dependency installation, and service startup.

**Security Baseline**

- **FR-015**: No credentials, API keys, or secrets MUST appear anywhere in the repository; all sensitive values MUST be loaded from environment variables.

#### Phase 1 Key Entities

- **Textbook Site**: The published frontend; key attributes are build status, three-level sidebar navigation (Module → Chapter → Section), and deployment URL.
- **Backend Service**: The API process; key attributes are health status, environment configuration, and registered route list.
- **Vector Store Collection**: The Qdrant collection for chapter embeddings; key attributes are collection name, accessibility, and schema version.
- **Relational Database**: Neon Postgres; key attributes are connection status, schema version, and applied migration history.

---

### Phase 1 Success Criteria


- **SC-001**: The textbook site builds with exit code 0 and zero broken internal links on every CI run.
- **SC-002**: The health endpoint returns HTTP 200 with all sub-checks passing within 2 seconds of a cold service start.
- **SC-003**: A developer unfamiliar with the project completes local setup from the README in under 15 minutes on Ubuntu 22.04.
- **SC-004**: The GitHub Pages deployment completes and the site is accessible at the published URL within 5 minutes of a merge to main.
- **SC-005**: The CI pipeline runs and completes on every pull request within 4 minutes.
- **SC-006**: Zero secrets or credentials appear in a full repository scan.

---

### Phase 1 Assumptions

- Ubuntu 22.04 is the primary development environment.
- GitHub Pages is the deployment target for the frontend (free tier, no additional infrastructure required).
- Qdrant Cloud Free Tier and Neon Serverless Postgres free tier are used throughout the project. Both are sufficient for the confirmed scale of 1–10 concurrent users.
- Docker is available in the development environment for the single-command local startup.
- The system is not designed for classroom or public scale. Load beyond 10 concurrent users is out of scope.

---

---

## Phase 2 — Base Features


### Overview

Deliver the three core deliverables: a fully chaptered Physical AI & Humanoid Robotics textbook, an embedded RAG chatbot that answers questions grounded in book content, and a selected-text mode that ties answers to user-highlighted passages.

---

### Phase 2 Non-Goals

The following are explicitly out of scope for Phase 2:

- User accounts, login, or session management (chat is anonymous in Phase 2)
- Content personalization or language translation
- Chat history persistence across separate browser sessions — within a single session, the last 3–5 exchanges are retained as rolling context (in scope); cross-session recall is not
- Multi-language content other than English
- Native mobile app — mobile web responsiveness is in scope
- Payment, certification, or progress-tracking features
- Subagent or agent-skill features — these are Phase 3

---

### Phase 2 Gates

**Entry criteria** (before Phase 2 work begins):
- Phase 1 SC-001 through SC-006 all pass
- The published site URL is stable and confirmed accessible
- Qdrant collection and Neon Postgres schema are confirmed accessible from the backend

**Exit criteria** (all must pass before Phase 3 begins):
- SC-001 through SC-008 all pass
- The 30-question golden evaluation set is authored, reviewed, and stored in the repository
- RAG benchmark has been run at least once against the golden set with results documented

---

### Phase 2 Ownership

| Deliverable | Owner Role |
|-------------|------------|
| Chapter first drafts (AI-generated from curriculum outline) | AI Editor (Claude Code) |
| Chapter technical accuracy review and correction | Domain Expert |
| Chapter style normalisation and final edit | AI Editor (Claude Code) |
| Content ingestion pipeline | Backend Lead |
| RAG endpoint and retrieval logic | Backend Lead |
| Chat UI component (embedded in chapters) | Frontend Lead |
| Selected-text detection and UI indicator | Frontend Lead |
| 30-question golden evaluation set | AI Lead + Domain Expert |
| RAG benchmark execution and scoring | AI Lead |
| Internal link validation | Frontend Lead |

---

### Phase 2 User Scenarios & Testing

#### User Story 1 — Student Reads the Textbook (Priority: P1)

A student navigates through the published site and reads complete, accurate, well-structured chapter content covering all four course modules (ROS 2, Gazebo/Unity, NVIDIA Isaac, VLA).

**Why this priority**: Textbook content is the primary deliverable. Without it, the RAG chatbot has nothing to retrieve.

**Independent Test**: Open all chapter pages in Chrome; verify each has a complete introduction, body content with code examples, and a summary. Run the internal link checker and confirm zero broken links.

**Acceptance Scenarios**:

1. **Given** the site is deployed, **When** a student opens Module 1 (ROS 2), **Then** the chapter loads with all required sections: learning objectives, concept explanations, at least one code example, and a chapter summary.
2. **Given** the sidebar navigation is rendered, **When** a student clicks any chapter link, **Then** the correct chapter renders within 2 seconds with no missing content or broken code blocks.
3. **Given** all four modules are published, **When** the internal link checker runs, **Then** zero broken internal links are reported and all 13 week-chapters each have their own page under the correct module in the sidebar.
4. **Given** the site is viewed on mobile Chrome, **When** a student navigates chapters, **Then** the layout is readable without horizontal scrolling and navigation works correctly.

---

#### User Story 2 — Student Asks the Chatbot a Question (Priority: P1)

A student opens any chapter page, types a question about the course content in the embedded chat panel, and receives a grounded, streaming answer with citations linking back to the relevant chapter section.

**Why this priority**: The RAG chatbot is the primary interactive feature of the textbook.

**Independent Test**: Submit the 30-question golden set via the chat interface; verify at least 27 return relevant, grounded answers with citations within 3 seconds each.

**Acceptance Scenarios**:

1. **Given** the chat panel is open, **When** a student submits a question about course content, **Then** a streaming response begins within 1 second and completes within 3 seconds, citing the relevant chapter section.
2. **Given** a question is answered, **When** the response is complete, **Then** at least one citation is displayed with a chapter and section reference linking to the source content.
3. **Given** a student asks a question unrelated to the textbook, **When** the response is generated, **Then** the chatbot states it can only answer questions about the course content rather than hallucinating an answer.
4. **Given** a network error occurs during streaming, **When** the student sees the error, **Then** a retry action is available that resubmits the exact prior question.
5. **Given** a student has asked two prior questions in the same session, **When** they ask a follow-up ("can you expand on point 2?"), **Then** the response demonstrates awareness of the prior exchange without the student restating context.

---

#### User Story 3 — Student Asks About Selected Text (Priority: P1)

A student highlights a passage in a chapter, asks a question about that specific excerpt in the chat panel, and receives an answer whose first paragraph directly addresses the selected text.

**Why this priority**: Selected-text Q&A is evaluated independently from the general chatbot.

**Independent Test**: Highlight 30 different passages across all modules and ask a question about each; verify at least 27 responses reference the selected context in their first paragraph within 3 seconds.

**Acceptance Scenarios**:

1. **Given** a student selects a paragraph and submits a question, **When** the response is generated, **Then** the first paragraph directly addresses the selected text before expanding to related content.
2. **Given** selected text is fewer than 20 characters, **When** the student submits a question, **Then** the system falls back to global retrieval and informs the student the selection was too short.
3. **Given** selected text is provided, **When** the response is displayed, **Then** a visual indicator shows which passage the answer is grounded in.
4. **Given** the student clears the selection, **When** they ask a new question, **Then** the chat returns to global retrieval mode.

---

#### User Story 4 — Chapter Content Is Indexed for Retrieval (Priority: P2)

A developer runs the content ingestion pipeline, and all chapter content is chunked, embedded, and stored in the vector store with correct chapter and section metadata.

**Why this priority**: Retrieval quality depends entirely on correct ingestion. Without accurate indexing, the chatbot fails the golden set evaluation.

**Independent Test**: After running ingestion, query the vector store for 5 representative questions; verify the correct chapter chunks appear in the top results for each.

**Acceptance Scenarios**:

1. **Given** the ingestion pipeline runs against all published chapters, **When** it completes, **Then** every chapter is represented in the vector store with correct chapter and section metadata on each chunk.
2. **Given** chunks are created at semantic boundaries, **When** a chunk is retrieved, **Then** it does not begin or end mid-sentence.
3. **Given** ingestion is re-run after a chapter update, **When** existing vectors are present, **Then** the pipeline updates only changed content rather than creating duplicate entries.

---

#### Phase 2 Edge Cases

- What happens when the chat endpoint is unavailable? The UI shows an inline error with the user's last message preserved and a retry button; it does not redirect or lose conversation state.
- What happens when retrieval returns no relevant results? The chatbot acknowledges the gap rather than hallucinating ("I couldn't find specific content on this topic in the textbook").
- What happens when a student submits an empty message? The send button is disabled; no request is made.
- What happens when selected text contains a code block? The system uses the enclosing section as context and preserves code block formatting in the response.
- What happens when a chapter is very long? Chunking splits at semantic boundaries and each chunk carries the correct parent chapter and section metadata regardless of chapter length.

---

### Phase 2 Requirements

#### Functional Requirements

**Textbook Content**

- **FR-001**: The system MUST publish a textbook organised in three levels: 4 Modules → ~13 Chapters (one per curriculum week) → Sections (H2/H3 headings within each chapter). The four modules are: ROS 2 Fundamentals (Weeks 1–5, 5 chapters), Simulation with Gazebo & Unity (Weeks 6–7, 2 chapters), NVIDIA Isaac Platform (Weeks 8–10, 3 chapters), and Vision-Language-Action / Humanoid Development (Weeks 11–13, 3 chapters).
- **FR-002**: Each chapter MUST contain: clearly stated learning objectives, a minimum of 3 titled sections with explanatory prose, at least one code example, and a chapter summary.
- **FR-003**: Minimum chapter length is 800 words of explanatory prose, excluding code blocks and headings. Each chapter follows a two-step authoring pipeline: (1) AI Editor (Claude Code) generates the first draft from the curriculum outline and weekly breakdown; (2) Domain Expert reviews and corrects for technical accuracy. A chapter MUST NOT be published until the Domain Expert review is complete.
- **FR-004**: All code examples MUST include a copy-to-clipboard action for the reader.
- **FR-005**: The site MUST be navigable on desktop and mobile in Chrome without horizontal scrolling.
- **FR-006**: The site MUST pass internal link validation with zero broken links before every deployment.

**RAG Chatbot**

- **FR-007**: The system MUST allow any anonymous user to submit a question and receive a grounded streaming response with at least one citation linking to the source chapter section. **Grounded** means every factual claim in the response is traceable to a chunk returned by the vector store for that request; no assertion is made from model-only knowledge. The LLM powering responses MUST be called via the OpenRouter API; the target model MUST be configurable via an environment variable (default: `meta-llama/llama-3.1-8b-instruct:free`).
- **FR-008**: Responses MUST begin streaming within 1 second of submission and complete within 3 seconds at p95 in the demo environment.
- **FR-009**: The chat panel MUST be embedded within chapter pages — not on a separate page — and accessible without login.
- **FR-010**: The chat panel MUST display output incrementally as the response streams, not all at once when complete.
- **FR-011**: The chat panel MUST support the states: idle, submitting, streaming, complete, and error — with transitions `idle → submitting → streaming → complete`, `submitting → error`, and `streaming → error`. A visible retry action in the error state MUST resubmit the exact prior question.
- **FR-012**: When retrieval finds no sufficiently relevant content, the system MUST respond with an explicit acknowledgment rather than generating a response that would fail the grounded definition (i.e., no claims from model-only knowledge). "Sufficiently relevant" is defined as at least one retrieved chunk with a cosine similarity score ≥ 0.70; if no chunk meets this threshold, the fallback acknowledgment MUST be returned.
- **FR-012a**: The system MUST maintain a rolling conversation window within a browser session: the last 5 exchanges (user question + assistant response pairs, reduced to 3 when the model context window is ≤8k tokens) MUST be included as context in every subsequent request in that session. The session ends when the browser tab is closed; no history carries across sessions.

**Selected-Text Q&A**

- **FR-013**: The system MUST detect when a user has selected text in a chapter page and display an indicator inviting them to ask a question about it.
- **FR-014**: When a question is submitted with selected text, the retrieval step MUST weight content from the same chapter and section more heavily than unrelated content.
- **FR-015**: When selected text is provided, the first paragraph of the generated response MUST directly address the selected passage.
- **FR-016**: If the selected text is fewer than 20 characters, the system MUST fall back to global retrieval and notify the user why.

**Content Ingestion**

- **FR-017**: The system MUST provide an ingestion pipeline that reads published chapter content, splits it into chunks at semantic boundaries, generates embeddings, and stores them in the vector store with chapter, section, and source-URL metadata on every chunk.
- **FR-018**: The ingestion pipeline MUST be idempotent — re-running it after a chapter update replaces changed chunks without creating duplicates. Each chunk is uniquely identified by the composite key `(chapterId, chunkIndex)`; the pipeline MUST upsert on this key, overwriting the existing vector and metadata at that position.
- **FR-019**: The embedding model used at ingestion time and at query time MUST be identical; the model identifier MUST be versioned in configuration.

**Cross-Cutting Constraints**

- **FR-020**: The chat endpoint MUST enforce a rate limit of 60 requests per minute per IP address. This limit is calibrated for demo scale (1–10 concurrent users) and must not be raised without re-evaluating free-tier capacity.
- **FR-021**: The backend MUST restrict cross-origin requests to the deployed frontend origin only.
- **FR-022**: All API error responses MUST follow the standard error model defined in the constitution: `apiVersion`, `requestId`, `error.code`, `error.message`.
- **FR-023a**: The system is explicitly scoped to a peak of 10 concurrent users. Qdrant Cloud Free Tier (1 collection, limited throughput) and Neon Serverless free tier are sufficient at this scale. Any load beyond 10 concurrent users is outside scope and may degrade performance without warning.

**30-Question Golden Evaluation Set**

- **FR-023**: A curated set of 30 questions MUST be authored and stored in the repository under `backend/tests/golden/` before the Phase 2 RAG benchmark is run. The set MUST cover all four modules (minimum 6 questions per module), include a mix of factual, conceptual, and troubleshooting prompts, and include the expected source section for each question. This set is the authoritative measure for SC-002, SC-004, SC-005, and SC-006.

#### Phase 2 Key Entities

- **Module**: A top-level curriculum grouping; 4 modules total. Key attributes are module ID, title, and ordered list of chapters.
- **Chapter**: One curriculum week's content page within a module; ~13 chapters total. Key attributes are chapter ID, parent module ID, week number, word count, and review status.
- **Section**: A headed division (H2 or H3) within a chapter. Key attributes are section ID, parent chapter ID, heading text, and heading level. Sections are the finest-grained unit cited by the chatbot.
- **Chunk**: A semantic segment of section text stored in the vector store; key attributes are text content, module ID, chapter ID, section ID, source URL, token count, and chunk index. The composite key `(chapterId, chunkIndex)` uniquely identifies a chunk for upsert operations.
- **Chat Exchange**: A question-and-answer pair within a session; key attributes are question text, selected text (optional), response text, citations, response latency, and position in the rolling window (max 5 exchanges retained per session).
- **Citation**: A reference to a source section; key attributes are chapter ID, section ID, and source URL.
- **Golden Question**: An evaluation question; key attributes are question text, expected source section ID, and difficulty category.

---

### Phase 2 Success Criteria


- **SC-001**: All four course modules are published with complete chapter content; zero internal broken links on build; every chapter meets the 800-word minimum.
- **SC-002**: At least 27 of 30 golden questions return responses that are grounded (every factual claim traceable to a retrieved chunk) and include at least one citation, scored by the AI Lead against the golden set.
- **SC-003**: The p95 chat response latency is at or below 3 seconds across the 30-question golden benchmark run.
- **SC-004**: At least 27 of 30 golden selected-text checks return a first paragraph that directly references the selected passage, verified by manual review.
- **SC-005**: Hallucination rate is at or below 10% on the golden set. Scoring uses three labels: **grounded** (all claims traceable to retrieved chunks), **uncertain** (claim not directly contradicted but not sourced to a retrieved chunk), **hallucinated** (claim contradicts or goes beyond retrieved chunks). Scored by manual review per response.
- **SC-006**: Recall@10 is at or above 0.80 on the golden set (the expected source chunk appears in the top-10 retrieval results for at least 24 of 30 questions).
- **SC-007**: The site renders correctly on desktop and mobile Chrome with no layout breakage, verified on both viewport sizes.
- **SC-008**: The content ingestion pipeline runs to completion without errors for all published chapters; every chunk in the vector store carries correct chapter and section metadata.

---

### Phase 2 Assumptions

- The target scale is 1–10 concurrent users (demo and judging panel only); free-tier infrastructure is sufficient and no horizontal scaling is required.
- The 30-question golden set is authored from real chapter content and does not include questions about content not yet written.
- The same embedding model is used for both ingestion and retrieval; model changes require a full re-index.
- "Semantic boundary" for chunking means a paragraph or heading break; mid-sentence splits are not acceptable.
- Chapter content is authored in Markdown/MDX within the Docusaurus docs directory; no external CMS is used.
- The AI Editor (Claude Code) generates all 13 chapter first drafts from the curriculum outline document and weekly breakdown before the Domain Expert review cycle begins.
- The Domain Expert is available and committed to review all 13 chapters before Phase 3 begins; if a chapter is not reviewed in time, it is excluded from the published site and golden evaluation set.
- The chatbot is anonymous in Phase 2; any personalization or profile-aware behavior is Phase 3 only.

---

---

## Phase 3 — Bonus Features


### Overview

Implement up to four bonus capabilities layered on top of the Phase 2 base: reusable agent skills, user authentication with background profiling, AI-driven content personalization per learner profile, and Urdu translation of chapter content.

**Priority order** (per constitution): Subagents → Better-Auth → Personalization → Urdu Translation.

**Winning rule**: Two bonuses executed excellently beats four bonuses executed poorly. A bonus feature that cannot be demonstrated reliably in 90 seconds must be cut before release.

---

### Phase 3 Non-Goals

The following are explicitly out of scope for Phase 3:

- Social/OAuth login providers (Google, GitHub) — email-and-password signup is the only required auth method
- Email address verification enforcement — the signup flow must not block access pending email confirmation
- Permanent storage of personalized content — personalization is session-scoped only; the canonical chapter content is never overwritten
- Real-time collaboration or multi-user editing
- Payment, subscription, or certification features
- Support for translation languages other than Urdu
- Automated grading of quiz results beyond immediate right/wrong feedback

---

### Phase 3 Gates

**Entry criteria** (before Phase 3 work begins):
- Phase 2 SC-001 through SC-008 all pass
- The 30-question golden set is complete and stored in the repository
- The RAG benchmark has passed

**Exit criteria** (all must pass before Phase 4 begins):
- SC-001 through SC-007 all pass for every bonus feature being shipped
- Any bonus feature not meeting its SC is formally cut and its UI entry point is hidden
- Auth-protected endpoints return HTTP 401 for unauthenticated requests, verified by automated test

---

### Phase 3 Ownership

| Deliverable | Owner Role |
|-------------|------------|
| Subagent implementations (quiz, summarizer, mapper) | AI Lead |
| Agent endpoint wiring and auth protection | Backend Lead |
| Better-Auth signup/signin flows | Full-Stack Lead |
| Profile questionnaire UI and data storage | Full-Stack Lead |
| Personalization endpoint and rewrite logic | AI Lead |
| Personalize button UI and inline content replacement | Frontend Lead |
| Translation endpoint | AI Lead |
| Translate button UI and inline content replacement + revert toggle | Frontend Lead |
| Urdu translation quality review | Domain Expert (Urdu-proficient reviewer) |
| Cut/keep decision for each bonus feature | Product Lead |

---

### Phase 3 User Scenarios & Testing

#### User Story 1 — Quiz Generator Agent (Priority: P1)

A logged-in student opens a chapter, requests a quiz, and receives a set of multiple-choice questions about that chapter's content — each with answer options, the correct answer, and an explanation.

**Why this priority**: Subagents demonstrate reusable intelligence beyond the base chatbot. The quiz generator is the most self-contained and highest-visibility agent.

**Independent Test**: As a logged-in user, request a 5-question quiz on any published chapter; verify 5 questions are returned with 4 options each, a marked correct answer, and an explanation, within 5 seconds.

**Acceptance Scenarios**:

1. **Given** a logged-in student opens Module 1 and requests a medium-difficulty quiz, **When** the quiz is generated, **Then** 5 multiple-choice questions about the chapter content appear within 5 seconds, each with 4 options, a marked correct answer, and an explanation.
2. **Given** the quiz is displayed, **When** a student selects answers and checks them, **Then** correct/incorrect feedback appears per question along with the explanation.
3. **Given** a quiz is requested on a chapter with insufficient content (fewer than 500 words), **When** the agent processes the request, **Then** a clear error is returned ("Insufficient content for a quiz on this section") and no questions are generated.
4. **Given** an anonymous user attempts to request a quiz, **When** the request is received, **Then** the system returns HTTP 401.

---

#### User Story 2 — Chapter Summarizer Agent (Priority: P1)

A logged-in student opens a chapter and requests a summary, receiving a concise overview with key points and citations adapted to their proficiency level.

**Why this priority**: The second subagent demonstrates breadth of the agent skill system and complements the quiz generator.

**Independent Test**: As a logged-in user with a beginner profile, request a summary of any chapter; verify the response contains a summary paragraph, at least 3 key points, and citations, within 5 seconds.

**Acceptance Scenarios**:

1. **Given** a student with a beginner profile requests a summary of Module 3, **When** the summary is returned, **Then** it uses accessible language, lists at least 3 key points, and cites the source sections.
2. **Given** a student with a software-engineer profile requests a summary, **When** the summary is returned, **Then** it emphasises integration and API concepts over hardware context.

---

#### User Story 3 — User Signup and Signin (Priority: P1)

A new student signs up with email and password, answers a background questionnaire during onboarding, and can subsequently sign in to access personalization, translation, and agent features.

**Why this priority**: Authentication gates the remaining three bonus features and is a required standalone deliverable.

**Independent Test**: Complete the full signup flow including profile questions, sign out, sign back in, confirm session persists for 24 hours, and verify protected endpoints return HTTP 401 for anonymous requests.

**Acceptance Scenarios**:

1. **Given** a new user completes registration and answers the three profile questions (Python level, ROS/robotics experience, AI knowledge level), **When** signup succeeds, **Then** their profile is stored and they are redirected to the homepage in an authenticated state.
2. **Given** an authenticated user closes the browser and reopens the site within 24 hours, **When** the site loads, **Then** the user is still signed in without re-entering credentials.
3. **Given** an anonymous user calls a protected endpoint, **When** the request is processed, **Then** the response is HTTP 401 with error code `AUTH_REQUIRED`.
4. **Given** a user submits invalid credentials, **When** the sign-in is attempted, **Then** a generic error is shown that does not reveal whether the email or the password is wrong.

---

#### User Story 4 — Content Personalization (Priority: P2)

A logged-in student clicks "Personalize" on a chapter section, and the prose is rewritten inline to match their learner track while all headings and code blocks remain unchanged.

**Why this priority**: Personalization directly demonstrates the AI-native textbook concept.

**Independent Test**: As a logged-in user with a software-engineer profile, personalize a section; verify the rewritten prose uses software-engineer voice and all headings and code blocks are byte-for-byte identical to the original.

**Acceptance Scenarios**:

1. **Given** a logged-in user with a software-engineer track clicks "Personalize" on a section, **When** the rewrite is returned, **Then** the section content is replaced inline, using software analogies, while all heading text, heading levels, and code blocks are structurally and textually identical to the original.
2. **Given** personalization completes, **When** the user refreshes the page, **Then** the canonical (non-personalized) content is shown — personalization is not persisted.
3. **Given** a user whose profile has unanswered questions clicks "Personalize", **When** the request is processed, **Then** the system defaults to the beginner track.

---

#### User Story 5 — Urdu Translation (Priority: P2)

A logged-in student clicks "Translate → Urdu" on a section, and the prose is replaced inline with Urdu text while all markdown formatting, headings, and code blocks are preserved structurally.

**Why this priority**: Urdu translation serves Panaversity's Pakistan-based student audience.

**Independent Test**: As a logged-in user, translate a section to Urdu; verify the output passes Urdu readability review, all heading levels and code blocks are unchanged, and no code block content is translated.

**Acceptance Scenarios**:

1. **Given** a logged-in user clicks "Translate → Urdu" on a section, **When** the translation is returned, **Then** the section is replaced inline with Urdu prose while all heading levels, bullet nesting, and code block fences are structurally identical to the original.
2. **Given** the section contains a code block, **When** translation is applied, **Then** the code block content is not translated — only surrounding prose is.
3. **Given** the translation is displayed, **When** the user clicks a revert control, **Then** the original English content is restored without a page reload.
4. **Given** an anonymous user requests a full-section translation, **When** the request is processed, **Then** the system returns HTTP 401.

---

#### Phase 3 Edge Cases

- What happens when an agent request times out (> 5 seconds)? The UI shows an error with a retry option; no partial output is displayed.
- What happens when Urdu translation takes longer than 5 seconds? A timeout error is shown and the original content remains unchanged.
- What happens if a bonus feature is broken? The feature's UI button is hidden rather than left in a broken state; the demo script is updated to skip it cleanly.
- What happens when a quiz is requested on a chapter with insufficient content? The agent returns a graceful error rather than generating hallucinated or low-quality questions.
- What happens if a student attempts to use a protected feature before signing in? The relevant UI button is either hidden or shows a "Sign in to use this feature" prompt — it never sends the request anonymously.

---

### Phase 3 Requirements

#### Functional Requirements

**Subagents**

- **FR-001**: The system MUST provide a quiz generator agent that accepts a chapter ID and difficulty level and returns a set of multiple-choice questions, each with options, the correct answer, and an explanation; grounded exclusively in that chapter's content.
- **FR-002**: The system MUST provide a chapter summarizer agent that accepts a chapter ID and proficiency level and returns a summary with at least 3 key points and source citations, adapted to the requested level.
- **FR-003**: The system MUST provide a prerequisite mapper agent that accepts a topic and chapter ID and returns a structured list of prerequisite concepts, each containing `concept` (string), `description` (string), and `sourceUrl` (string pointing to a real chapter section). The list MUST contain at least 2 items when the topic has identifiable prerequisites.
- **FR-004**: All agent features MUST require authentication; unauthenticated requests MUST receive HTTP 401.
- **FR-005**: Agent responses MUST be grounded in chapter content retrieved from the vector store — every factual claim must be traceable to a retrieved chunk; agents MUST NOT generate answers based solely on general model knowledge. All agents MUST be implemented using the OpenAI Agents SDK (`openai-agents` Python package) as the orchestration framework, with LLM calls routed through OpenRouter via a custom model provider. The target model MUST be configurable via the same environment variable as the RAG chatbot (FR-007 in Phase 2).

**Authentication**

- **FR-006**: The system MUST provide signup and signin flows using the Better-Auth library with email-and-password as the authentication method.
- **FR-007**: During signup, the system MUST collect a three-question background profile: Python proficiency level (beginner/intermediate/advanced), ROS/robotics experience (yes/no), and AI/ML knowledge level (beginner/intermediate/advanced).
- **FR-008**: The collected profile MUST be stored in the relational database and associated with the user account for use by personalization and agent features.
- **FR-009**: Session tokens MUST have a TTL of 24 hours; the user is not required to re-authenticate within that window.
- **FR-010**: Protected endpoints (personalization, translation, all agent endpoints) MUST return HTTP 401 with error code `AUTH_REQUIRED` for unauthenticated requests.
- **FR-011**: Protected UI buttons (Personalize, Translate, Quiz) MUST be hidden or disabled for unauthenticated users.
- **FR-012**: Sign-in error messages MUST NOT reveal whether the email or the password is incorrect.

**Personalization**

- **FR-013**: The system MUST provide a personalization feature that rewrites a chapter section's explanatory prose to match a learner's profile track and proficiency level.
- **FR-014**: Rewritten content MUST preserve all heading text, heading levels, code block content, and code block fences exactly — only explanatory prose is rewritten.
- **FR-015**: The system MUST support four personalization tracks: beginner, software engineer, hardware/robotics, and accelerated. Each track has a distinct rewriting voice as defined in the constitution's adaptive learning paths section. The active track MUST be derived from the user's stored profile using the following priority-ordered rules table (first matching rule wins):

  | Priority | ROS Experience | Python Level | AI Knowledge | → Track |
  |----------|---------------|--------------|--------------|---------|
  | 1 | yes | any | any | hardware/robotics |
  | 2 | no | advanced | intermediate or advanced | accelerated |
  | 3 | no | intermediate or advanced | any | software engineer |
  | 4 | (default) | any | any | beginner |
- **FR-016**: The Personalize button MUST replace section content inline without a full page reload.
- **FR-017**: Personalization MUST be session-scoped; a page refresh restores the canonical content.
- **FR-018**: If a user's profile is incomplete, the system MUST default to the beginner track.

**Personalization Quality Standard**

A personalized output is considered correct if it passes all three of these checks:
1. All headings are identical (same text, same level) to the original.
2. All code blocks are identical (same content, same fence markers) to the original.
3. The rewritten prose demonstrably reflects the requested track: beginner output uses plain analogies; software-engineer output emphasises APIs and code patterns; hardware/robotics output emphasises sensors and control loops; accelerated output is condensed and skips introductory scaffolding.

**Urdu Translation**

- **FR-019**: The system MUST provide a translation feature that translates a chapter section's prose into Urdu.
- **FR-020**: Translated output MUST preserve all heading levels, bullet nesting, bold/italic markers, and code block fences structurally — only prose is translated.
- **FR-021**: Code block content MUST NOT be translated; fences and language tags MUST remain unchanged.
- **FR-022**: The UI MUST provide a revert control that restores the original English content without a page reload.
- **FR-023**: Translation quality MUST be reviewed by a Urdu-proficient reviewer on at least 2 sample sections before the feature is considered demo-ready.

**Cross-Cutting Constraints**

- **FR-024**: All protected endpoints MUST follow the standard error model from the constitution: `apiVersion`, `requestId`, `error.code`, `error.message`.
- **FR-025**: Agent endpoints MUST enforce a rate limit of 20 requests per minute per authenticated user.
- **FR-026**: The personalize endpoint MUST complete within 5 seconds at p95 in the demo environment.
- **FR-027**: The translate endpoint MUST complete within 5 seconds at p95 in the demo environment.
- **FR-028**: All agent endpoints MUST complete within 5 seconds at p95 in the demo environment.

#### Phase 3 Key Entities

- **User**: Registered learner; key attributes are email, hashed credential, profile track, proficiency levels, and session expiry.
- **User Profile**: Background data collected at signup; key attributes are Python level, ROS experience (boolean), AI knowledge level, and derived personalization track. The derived track is computed at read time from the rules table in FR-015; it is not stored separately.
- **Agent Invocation**: A single agent call; key attributes are agent name, chapter ID, input parameters, grounding chunks retrieved, output, and latency.
- **Personalized Section**: A rewritten content block; key attributes are chapter ID, section ID, original markdown, applied profile track, and rewritten markdown.

---

### Phase 3 Success Criteria


- **SC-001**: The quiz generator returns a full set of valid multiple-choice questions with correct answers and explanations for any published chapter within 5 seconds.
- **SC-002**: The chapter summarizer returns a summary with at least 3 key points and citations within 5 seconds.
- **SC-003**: The full signup → profile questionnaire → signin → protected feature access flow completes without errors across 5 consecutive test runs.
- **SC-004**: An authenticated session persists across a browser close and reopen within 24 hours; unauthenticated requests to all protected endpoints return HTTP 401.
- **SC-005**: The personalization feature rewrites prose to match the requested track while all headings and code blocks pass the three-point quality standard; verified for all 4 tracks on at least 2 sample sections.
- **SC-006**: The translation feature produces output that passes Urdu readability review on at least 2 sections, with zero translated code blocks and `formatPreserved` confirmed by structural comparison; p95 latency at or below 5 seconds.
- **SC-007**: All bonus features being shipped are demonstrable in the 90-second demo without authentication failures or timeouts across 3 consecutive rehearsal runs.

---

### Phase 3 Assumptions

- Email verification is not enforced; users are not blocked pending confirmation.
- Personalization uses the user's stored profile from signup by default; a temporary track override via a UI dropdown is allowed without re-registering.
- The Urdu translation quality reviewer is available to evaluate at least 2 sections.
- The three subagents (quiz generator, summarizer, prerequisite mapper) collectively satisfy the subagent bonus; the quiz generator alone is sufficient for a reduced partial demonstration if the others are not ready.
- Any bonus feature not meeting SC is cut per the feature freeze policy.

---

---

## Phase 4 — Demo Video, Polish & Submission


### Overview

Finalize all artifacts for submission: a stable demo environment, a rehearsed 90-second demo video, a complete submission package, and tested contingency plans for each likely failure scenario. This phase is about hardening and packaging — no new features are introduced here.

---

### Phase 4 Non-Goals

The following are explicitly out of scope for Phase 4:

- New features or feature enhancements of any kind (feature freeze applies)
- Schema changes, database migrations, or dependency upgrades before submission
- Multi-region deployment or production infrastructure beyond what is needed for a single stable demo URL
- Automated end-to-end test suite
- Post-submission roadmap work or production hardening

---

### Phase 4 Gates

**Entry criteria** (before Phase 4 work begins):
- Phase 3 cut/keep decisions are finalised
- All features being shipped meet their Phase 3 exit criteria
- The demo environment is running and reachable at stable URLs

**Exit criteria** (all must pass before submission):
- SC-001 through SC-008 all pass
- Submission form is completed and confirmation receipt is saved 

---

### Phase 4 Ownership

| Deliverable | Owner Role |
|-------------|------------|
| Demo script (written, timed) | Demo Owner |
| Demo rehearsals (5 runs minimum) | Demo Owner + Presenter |
| Contingency artifact preparation (4 scenarios) | Demo Owner |
| Backend deployment and health check | DevOps Owner |
| Frontend deployment (GitHub Pages) | Frontend Lead |
| Rollback procedure documentation and dry run | DevOps Owner |
| Demo video recording and editing | Demo Owner |
| Submission form completion | Product Lead |
| Repository visibility verification (public) | Architecture Lead |
| README final update (URLs, video link, architecture) | Architecture Lead |

---

### Phase 4 User Scenarios & Testing

#### User Story 1 — Judge Watches the Demo Video (Priority: P1)

A judge watches the demo video and sees, within 90 seconds: the published textbook site, the RAG chatbot answering a grounded question with citations, the selected-text feature, and at least two bonus features.

**Why this priority**: The demo video is the single highest-leverage artifact — judges evaluate it first and it determines live presentation invitations.

**Independent Test**: Watch the video with a timer; verify every required feature appears in its designated time window, all UI elements are legible, and total runtime is 90 seconds or fewer.

**Acceptance Scenarios**:

1. **Given** the demo video is playing, **When** the 15-second mark is reached, **Then** the Docusaurus homepage and at least one module page are visible with chapter navigation shown.
2. **Given** the demo video plays from 15 to 35 seconds, **When** a text passage is highlighted and a question is submitted, **Then** the chatbot response streams on screen with at least one citation link visible.
3. **Given** the demo video plays from 35 to 70 seconds, **When** at least two bonus features are demonstrated, **Then** each shows a clear before/after or interaction outcome without authentication errors or visible loading failures.
4. **Given** the demo video plays from 70 to 90 seconds, **When** the repository and architecture are shown, **Then** the repository URL, a system architecture diagram, and the live app URL are readable on screen.
5. **Given** the completed video is measured, **When** timing is verified, **Then** total runtime is 90 seconds or fewer.

---

#### User Story 2 — Deployment Is Stable (Priority: P1)

Both the frontend and backend are deployed to stable, unchanging URLs; the health endpoint passes 3 consecutive checks at 1-minute intervals; and a tested rollback procedure exists for the backend.

**Why this priority**: A single deployment failure during the live presentation nullifies all development work.

**Independent Test**: Run 3 consecutive health checks at 1-minute intervals confirming HTTP 200. Execute the rollback procedure once from scratch and verify the prior stable version is restored and health-checked within 5 minutes.

**Acceptance Scenarios**:

1. **Given** the backend is deployed, **When** the health endpoint is called 3 times at 1-minute intervals, **Then** all 3 responses return HTTP 200 with all sub-checks healthy.
2. **Given** the frontend is deployed, **When** the published URL is opened, **Then** the site loads within 3 seconds with no console errors and all chapter navigation works.
3. **Given** a simulated deployment failure, **When** the rollback command is executed, **Then** the previous stable version is live and health-checked within 5 minutes.

---

#### User Story 3 — Submission Package Is Complete (Priority: P1)

A team member submits all four required artifacts before the deadline: public GitHub repo link, live deployment URL, demo video link (under 90 seconds), and WhatsApp number.

**Why this priority**: Missing any required submission artifact results in disqualification regardless of technical quality.

**Independent Test**: Open the submission form, verify all four fields are correctly filled, confirm the repo is public, the deployment URL loads the textbook, and the video is publicly accessible and under 90 seconds.

**Acceptance Scenarios**:

1. **Given** the GitHub repository has been verified as public, **When** its URL is opened by an anonymous reviewer, **Then** the full repository is visible and can be cloned.
2. **Given** the demo video link is submitted, **When** it is opened without authentication, **Then** the video plays and its runtime is 90 seconds or fewer.
3. **Given** the deployment URL is submitted, **When** a judge visits it, **Then** the textbook site loads and the chatbot responds to a test question.
4. **Given** the form is submitted, **When** the submission is confirmed, **Then** a confirmation receipt (email or screenshot) is saved as proof before the deadline.

---

#### User Story 4 — Contingency Plans Are Rehearsed (Priority: P2)

During rehearsals, the team simulates each of the four failure scenarios and pivots to the contingency plan in each case without exceeding 90 seconds.

**Why this priority**: Live demos have a high failure rate. Rehearsed contingencies make the score independent of live system reliability.

**Independent Test**: Rehearse 5 runs with a timer; in at least 2 runs, inject a simulated failure; verify the contingency path is used smoothly and total time stays within 90 seconds.

**Acceptance Scenarios**:

1. **Given** the chat API is unavailable during rehearsal, **When** the presenter switches to the pre-loaded fallback screenshot, **Then** the demo continues with no pause exceeding 5 seconds and the screenshot shows a citation-backed response.
2. **Given** the auth flow fails during rehearsal, **When** the presenter switches to the pre-authenticated backup browser tab, **Then** the personalization or agent feature is demonstrated successfully.
3. **Given** the translation endpoint times out during rehearsal, **When** the presenter shows the pre-generated Urdu output artifact, **Then** the translated section with preserved formatting is visible.
4. **Given** all 5 rehearsals are run with a timer, **When** the results are reviewed, **Then** at least 4 of 5 runs complete within 90 seconds.

---

#### Phase 4 Edge Cases

- What happens if GitHub Pages propagation is delayed? The presenter uses a locally served static export as fallback and states the propagation is in progress.
- What happens if the demo video exceeds 90 seconds after editing? It must be re-edited before submission; judges stop watching at the 90-second mark.
- What happens if the backend deployment URL changes after the video is recorded? No URL changes are permitted after recording; the demo script is locked to the final stable URL.
- What happens if the GitHub repo is accidentally made private the day before submission? A public-visibility check must be run before submission.

---

### Phase 4 Requirements

#### Functional Requirements

**Demo Video**

- **FR-001**: The demo video MUST be 90 seconds or fewer in total runtime, verified with a video editor timestamp before submission.
- **FR-002**: The video MUST show the textbook homepage and chapter navigation within the first 15 seconds.
- **FR-003**: The video MUST demonstrate the RAG chatbot returning a grounded, streaming response with at least one visible citation within the 15–35 second window.
- **FR-004**: The video MUST demonstrate the selected-text feature (user highlights text, asks a question, chatbot references the selection) within the 15–35 second window.
- **FR-005**: The video MUST demonstrate at least two bonus features within the 35–70 second window, each showing a clear interaction outcome.
- **FR-006**: The video MUST show the GitHub repository URL, an architecture diagram, and the live app URL within the 70–90 second window, with all text legible.
- **FR-007**: The video MUST use screen recording with audio narration; all on-screen text must be legible at 1080p or higher.
- **FR-008**: The video link MUST be publicly accessible without authentication (YouTube, Loom, or equivalent).

**Deployment**

- **FR-009**: The textbook site MUST be deployed to GitHub Pages at a stable URL unchanged through submission.
- **FR-010**: The backend MUST be deployed to Render (free tier) at a stable public URL with a working health endpoint; the Render service name and URL MUST be documented in the README.
- **FR-011**: A rollback procedure for the backend MUST be written, version-controlled, and executed as a dry run at least once before the demo video is recorded. The rollback method is Render's "Deploy a specific commit" feature via the dashboard; the procedure document MUST include the exact steps.
- **FR-012**: The deployment MUST pass 3 consecutive health checks at 1-minute intervals with HTTP 200 before the demo video is recorded.
- **FR-013**: A static fallback demo page MUST exist at a known URL containing the architecture diagram, feature list, and a pre-recorded walkthrough clip for use if live deployment fails entirely.

**Demo Script & Rehearsal**

- **FR-014**: A written demo script MUST exist documenting narrator speech, user actions, and timing for all five segments (0–15s, 15–35s, 35–55s, 55–70s, 70–90s).
- **FR-015**: The demo MUST be rehearsed at least 5 times with a timer before the video is recorded.
- **FR-016**: Four fallback artifacts MUST be prepared and verified before the demo video is recorded:
  - A pre-loaded screenshot of a successful chat response with citations (for API unavailability)
  - A pre-authenticated backup browser tab with personalization or agent feature accessible (for auth failure)
  - A pre-generated translated section showing preserved Urdu formatting (for translation timeout)
  - A static fallback page at a known URL (for full deployment failure)
- **FR-017**: The demo MUST have a single narrator and at most two visible browser tabs at any point.

**Submission**

- **FR-018**: The GitHub repository MUST be verified as publicly accessible before the submission form is submitted.
- **FR-019**: The README MUST be updated with the live deployment URL, demo video link, and an architecture overview before submission.
- **FR-020**: The submission form MUST be completed with all four required fields (GitHub repo URL, deployment URL, demo video link, WhatsApp number).

**Feature Freeze Compliance**

- **FR-021**: No new feature classes MUST be introduced once development is complete.
- **FR-022**: No schema changes or dependency upgrades MUST be made once development is complete.
- **FR-023**: Any bonus feature that is unstable MUST have its UI entry point removed or disabled and MUST be excluded from the demo script.

#### Phase 4 Key Entities

- **Demo Script**: A written document with timed segments, narrator speech, user actions, and fallback transitions; locked before recording.
- **Submission Package**: The four submitted artifacts: repository URL, deployment URL, video link, and contact number.
- **Fallback Artifact**: A pre-generated asset (screenshot, pre-recorded clip, or static page) for use when a live feature fails.
- **Deployment Health Record**: Timestamped evidence of 3 consecutive HTTP 200 health check responses, captured before recording.
- **Confirmation Receipt**: Proof of form submission (email confirmation or screenshot) saved before the deadline.

---

### Phase 4 Success Criteria

- **SC-001**: The demo video runtime is 90 seconds or fewer, confirmed with a video editor timestamp before submission.
- **SC-002**: All five demo segments (homepage, RAG+selected-text, bonus feature 1, bonus feature 2, architecture) appear in their designated time windows and are legible.
- **SC-003**: The deployment health check passes 3 consecutive times at 1-minute intervals with HTTP 200, timestamped evidence saved before recording.
- **SC-004**: The rollback procedure is executed as a dry run at least once and restores a prior stable version within 5 minutes.
- **SC-005**: The demo script is rehearsed at least 5 times, with at least 4 runs completing within 90 seconds.
- **SC-006**: Each of the four fallback artifacts is prepared, stored in a known location, and confirmed usable in at least one rehearsal run.
- **SC-007**: The GitHub repository is confirmed publicly accessible and the README contains the deployment URL, video link, and architecture overview.
- **SC-008**: The submission form is completed with all four required fields and a confirmation receipt is saved 

---

### Phase 4 Assumptions

- The demo video is pre-recorded and submitted via link; the live Zoom presentation is by invitation only.
- The backend is deployed on Render (free tier). Render's auto-deploy-from-GitHub and "Deploy a specific commit" rollback feature satisfy FR-010 and FR-011 without additional tooling.
- Deployment is sized for 1–10 concurrent users. "Stable" means the health endpoint passes 3 consecutive checks at the confirmed demo scale, not production-grade uptime guarantees.
- The architecture diagram may be a hand-drawn or tool-generated block diagram; it does not need to be auto-generated from code.
