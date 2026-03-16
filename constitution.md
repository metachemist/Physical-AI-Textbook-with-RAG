# Physical AI & Humanoid Robotics Textbook – Hackathon Optimized Constitution v2.1

## Project Readiness Dashboard

- Base: In Progress
- RAG: In Progress
- Selected Text: In Progress
- Auth: Pending
- Personalization: In Progress
- Urdu: Pending
- Demo: Pending
- Deployment: In Progress

### Definition of Done (Operational)

| Area | Owner | Deadline | Pass Criteria |
|------|-------|----------|---------------|
| Base | Product Lead | T-5 days | Docusaurus book published, 0 broken internal links in docs build, required pages complete, and chapter navigation works across desktop + mobile in latest Chrome |
| RAG | Backend Lead | T-5 days | Golden set >= 30/30 answered, relevance review >= 85%, p95 latency <= 3s |
| Selected Text | Frontend Lead | T-4 days | Selected text is sent to `/api/v1/chat` in payload and first response paragraph references selected context in >= 27/30 golden selected-text checks |
| Auth | Full-Stack Lead | T-4 days | Better-Auth login/logout works, protected routes enforced, session persistence verified |
| Personalization | AI Lead | T-3 days | `/api/v1/personalize` returns scoped rewrite preserving headings/code blocks |
| Urdu | AI Lead | T-3 days | `/api/v1/translate` produces Urdu while preserving markdown structure |
| Demo | Demo Owner | T-2 days | 90-second script rehearsed 5 times, no step exceeds allocated window |
| Deployment | DevOps Owner | T-2 days | Frontend + backend deployed to stable demo URLs, `/health` returns 200 for 3 consecutive checks at 1-minute intervals, and rollback command validated once |

---

## Vision

Build an AI-native, student-centered textbook for Physical AI and Humanoid Robotics that is practical, interactive, and demo-ready for Panaversity Hackathon I.

This constitution defines how the team wins the hackathon by:
- Shipping required base functionality with high reliability.
- Executing two or more bonus features at high quality.
- Presenting a clear 90-second demo that judges can score quickly.

---

## Official Hackathon Requirements

### Mandatory Deliverables (Base 100)

1. Docusaurus-based textbook website.
2. RAG chatbot integrated into the book.
3. Selected-text question answering (context-aware chat mode).

### Required Technical Stack

- Frontend: Docusaurus
- Backend: FastAPI
- Agent Framework: OpenAI Agents SDK
- Relational Database: Neon Postgres
- Vector Database: Qdrant Cloud
- Workflow Tooling: Claude Code + Spec-Kit Plus

### Optional Bonus Features (Up to +200)

- Subagents (+50)
- Better-Auth (+50)
- Personalization (+50)
- Urdu Translation (+50)

### Non-Negotiable Alignment Rules

- No substitution away from the required stack for base capabilities.
- Claude Code + Spec-Kit Plus is the standard development workflow.
- Demo must remain under 90 seconds.

### Judging Evidence Matrix

| Requirement | Implementation Location | Demo Timestamp | Proof Link |
|------------|--------------------------|----------------|------------|
| Docusaurus book | `frontend/docs/` | 0-15s | GitHub repo + live URL |
| RAG chatbot | `backend/app/api/chat.py` | 15-35s | API docs + chat recording |
| Selected text Q&A | `frontend/src/components/ChatPanel/` + `/api/v1/chat` | 15-35s | Screen capture showing selected text payload |
| Subagents (bonus) | `backend/app/api/agents.py` | 35-55s | Agent endpoint output in repo/video |
| Better-Auth (bonus) | `auth/index.ts` + protected routes | 35-55s or fallback clip | Login flow capture |
| Personalization (bonus) | `backend/app/api/personalize.py` | 55-70s | Before/after section capture |
| Urdu translation (bonus) | `backend/app/api/translate.py` | 55-70s | Side-by-side output capture |

---

## Scope and Success Criteria

### In Scope

- Publish chaptered robotics curriculum in Docusaurus.
- Implement `/api/v1/chat` with retrieval-augmented responses.
- Support selected-text mode from chapter content.
- Implement at least two bonus features to a demonstrable standard.
- Produce a concise, high-clarity demo with reproducible flow.

### Out of Scope

- Physical robot manufacturing or hardware fabrication.
- Production-grade multi-region infrastructure.
- Enterprise SSO and advanced compliance controls.

### Success Metrics

- Base features fully operational and demoed end-to-end.
- RAG grounding >= 27/30 golden queries (every factual claim traceable to a retrieved chunk).
- Hallucination rate <= 10% during demo benchmark set.
- First meaningful interaction within 3 seconds on demo environment.
- Demo duration <= 90 seconds.

---

## Hackathon Scoring Strategy (300 Points)

### Score Model

- Base (100): Docusaurus Book (40) + RAG Chatbot (40) + Selected Text Q&A (20)
- Bonus (200): Subagents (50) + Better-Auth (50) + Personalization (50) + Urdu (50)

### Winning Prioritization

1. Lock Base 100 early.
2. Deliver Subagents + Better-Auth next (fastest high-signal bonus pair).
3. Add Personalization or Urdu as third bonus depending on stability.
4. Polish UX and tighten demo narrative.

### Strategic Principle

Base + 2 bonuses executed excellently beats all 4 bonuses executed poorly.

---

## Project Timeline

### Phase 1: Setup + Infrastructure

- Repository structure finalized.
- Docusaurus content pipeline active.
- FastAPI service skeleton and Qdrant/Neon connections validated.

### Phase 2: Base Features (Target 100)

- Chapter rendering finalized.
- RAG endpoint passes 30/30 golden queries with API error rate < 2% across 3 rehearsal runs.
- Selected-text flow integrated in UI.

### Phase 3: Bonuses (Target 150+)

- Subagents and Better-Auth first.
- Personalization or Urdu next based on risk.

### Phase 4: Demo Video + Polish

- Script rehearsal, timing lock, UI cleanup, failure fallback plan.

### Final: Submission + Presentation Prep

- Repository, video, and form submission complete.
- Backup demo path prepared.

### Milestone Gates

- T-7 days: Base architecture complete, sample chapter + chat path functional.
- T-5 days: Base scoring path locked (Docusaurus + RAG + selected text).
- T-4 days: First two bonus features decision finalized.
- T-3 days: RAG benchmark pass against golden set.
- T-2 days: Final demo script lock and dry run acceptance.
- T-1 day: Submission artifacts freeze and upload verification.

### Feature Freeze Policy

- T-72h: No new feature classes introduced.
- T-48h: Any failing bonus can be cut; base path cannot be modified except bug fixes.
- T-24h: Demo-only fixes allowed; no schema changes, no dependency upgrades.

---

## Architecture (Lean Hackathon Design)

### System Overview

- Docusaurus serves chapter content and interactive UI components.
- FastAPI serves RAG, personalization, translation, and agent endpoints.
- Qdrant stores embeddings and retrieval metadata.
- Neon stores users, sessions, and feature state.
- OpenAI Agents SDK runs subagents for scoped educational tasks.

### Repository Structure

```text
/
├── constitution.md
├── frontend/
│   ├── docs/                    # Chapters (MD/MDX)
│   │   ├── module-1-ros2/
│   │   ├── module-2-simulation/
│   │   ├── module-3-nvidia-isaac/
│   │   └── module-4-vla-humanoid/
│   ├── src/components/
│   │   ├── ChatPanel/
│   │   └── AuthModal/
│   ├── docusaurus.config.ts
│   └── sidebars.ts
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── dependencies.py
│   │   ├── api/               # Route handlers
│   │   ├── services/          # Business logic
│   │   └── db/                # Database access
│   ├── alembic/
│   └── tests/
├── auth/                        # Better-Auth microservice (Phase 3)
│   ├── index.ts
│   └── package.json
└── .github/workflows/
```

### API Surface (v1)

- `POST /api/v1/chat`
- `POST /api/v1/personalize`
- `POST /api/v1/translate`
- `POST /api/v1/agents/{agentName}`

### Endpoint Contracts (Implementation-Ready)

#### `POST /api/v1/chat`

Auth:
- Optional; authenticated requests may include profile/session context.

Request:
```json
{
  "message": "Explain ROS 2 DDS in simple terms",
  "conversationId": "conv_001",
  "chapterId": "module-1-ros2",
  "selectedText": "ROS 2 uses DDS middleware for pub/sub communication.",
  "stream": true
}
```

Response:
```json
{
  "apiVersion": "v1",
  "requestId": "req_chat_001",
  "answer": "ROS 2 uses DDS as the communication layer...",
  "citations": [
    {
      "chapterId": "module-1-ros2",
      "sectionId": "dds-overview",
      "sourceUrl": "/docs/module-1/dds-overview"
    }
  ],
  "latencyMs": 1840
}
```

Latency target:
- p95 <= 3000ms in demo environment.

#### `POST /api/v1/personalize`

Auth:
- Required.

Request:
```json
{
  "chapterId": "module-3-isaac",
  "sectionId": "vslam-basics",
  "sourceMarkdown": "## VSLAM\\n..."
}
```

Response:
```json
{
  "apiVersion": "v1",
  "requestId": "req_per_001",
  "personalizedMarkdown": "## VSLAM\\nThis section explains...",
  "appliedTrack": "software_engineer"
}
```

Latency target:
- p95 <= 5000ms.

#### `POST /api/v1/translate`

Auth:
- Required.

Request:
```json
{
  "sourceMarkdown": "### Sensor Fusion\\n...",
  "scope": "section",
  "chapterId": "module-2-simulation",
  "sectionId": "sensor-fusion",
  "targetLanguage": "ur"
}
```

Response:
```json
{
  "apiVersion": "v1",
  "requestId": "req_tr_001",
  "translatedMarkdown": "### سینسر فیوژن\\n...",
  "formatPreserved": true
}
```

Latency target:
- p95 <= 5000ms.

#### `POST /api/v1/agents/{agentName}`

Auth:
- Required.

Request:
```json
{
  "input": {
    "chapterId": "module-4-vla",
    "difficulty": "medium",
    "count": 5
  }
}
```

Response:
```json
{
  "apiVersion": "v1",
  "requestId": "req_agent_001",
  "agentName": "quiz_generator",
  "output": {
    "questions": [
      {
        "question": "What is VLA?",
        "options": ["A", "B", "C", "D"],
        "answer": "B",
        "explanation": "..."
      }
    ]
  }
}
```

Latency target:
- p95 <= 5000ms.

### Minimal Deployment Pattern

- Frontend: GitHub Pages
- Backend: one deployable FastAPI service
- Single managed Qdrant collection + one Neon database

---

## Hackathon Mode

### Delivery Rules

- Simplified CI/CD: lint + smoke test + manual approval.
- Single environment: one stable demo environment.
- Manual deploy allowed before final demo lock.
- Monitoring optional: basic health checks only.
- Focus: demo-critical features over infrastructure perfection.

### Required Controls

- One-click rollback plan for backend.
- One static fallback path for frontend demo page.
- Daily checkpoint on demo script viability.

---

## Production Mode (Post-Hackathon)

- Multi-environment promotion (dev/stage/prod).
- Full CI with integration and regression gates.
- Observability stack (metrics, logs, traces).
- Security hardening and retention governance.
- Scalability optimizations and cost controls.

---

## Frontend Experience Specification

### Chapter Rendering

- Source format: MD/MDX in Docusaurus.
- Heading hierarchy must be valid and consistent.
- Code blocks require language tags and copy action.
- Component overrides are centralized under `src/theme` and `src/components`.

### AI Chat UX Contract

State model:
- `idle -> submitting -> streaming -> complete`
- `submitting -> error`
- `streaming -> error`

Requirements:
- Streaming output appears incrementally.
- Retry action resubmits exact prior payload.
- Error banner remains inline with user message preserved.

### Event to Action Mapping

- Select text + ask question -> call `POST /api/v1/chat` with `selectedText`.
- Click Personalize -> call `POST /api/v1/personalize` and replace scoped content block.
- Click Translate -> call `POST /api/v1/translate` and replace scoped content block.

---

## Backend and RAG Specification

### RAG Pipeline

1. Ingest chapter content from Docusaurus docs.
2. Chunk by semantic boundaries (target 600-900 tokens, overlap 100).
3. Generate embeddings and upsert to Qdrant with chapter metadata.
4. Retrieve top-k candidates (`k=10`) with optional chapter and selected-text boost.
5. Re-rank to top-n context (`n=4-6`).
6. Generate answer with citation-aware prompt.

### Selected-Text Mode

- If `selectedText` present, retrieval scoring boosts same section/chapter chunks.
- First paragraph must directly address selected context.
- If selected text invalid (<20 chars), fallback to global retrieval.

### Agent Skills (OpenAI Agents SDK)

1. `chapter_summarizer`
- Input: `chapterId`, `level`
- Output: concise summary + key points + citations

2. `quiz_generator`
- Input: `chapterId`, `difficulty`, `count`
- Output: multiple-choice quiz set + explanations

3. `prerequisite_mapper`
- Input: `topic`, `chapterId`
- Output: prerequisite concepts + recommended sections

### Authentication and Authorization Rules

- `chat`: anonymous allowed; authenticated improves context memory.
- `personalize`, `translate`, `agents/*`: authenticated required.

### Standard Error Model

```json
{
  "apiVersion": "v1",
  "requestId": "req_xxx",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable reason",
    "details": {}
  }
}
```

Common codes:
- `AUTH_REQUIRED`
- `VALIDATION_ERROR`
- `RATE_LIMITED`
- `NOT_FOUND`
- `INTERNAL_ERROR`

---

## Adaptive Learning Paths

### Beginner Path (No ROS Background)

- Simplified terminology.
- Extra conceptual analogies.
- More visual explainers, fewer assumptions.

### Software Engineer Path

- Emphasis on APIs, middleware, inference pipelines, and code patterns.
- Deeper coverage of ROS integration from software-first angle.

### Hardware/Robotics Path

- Emphasis on sensors, control loops, simulation fidelity, and embodiment constraints.
- Bridge sections connecting mechanical context to AI behavior.

### Accelerated Track

- Condensed chapter summaries.
- Advanced challenges and capstone-first sequence.

### Personalization Link

User profile drives path selection and adaptation level for each chapter via `POST /api/v1/personalize`.

---

## Low-Resource / Cloud-Only Mode

### Strategic Goal

Ensure students without high-end local hardware can complete core learning and see full capability.

### Mode Definition

- Cloud-only labs for all mandatory exercises.
- Pre-recorded Isaac demonstrations embedded in chapters.
- Dataset-driven simulation tasks when live simulation is unavailable.
- Simulation-first fallback for all hardware-heavy modules.
- Browser-friendly mode with lightweight assets and reduced compute operations.

### Competitive Advantage

- Broader accessibility.
- Fewer demo failures from local device constraints.
- Strong educational equity narrative for judges.

---

## RAG Evaluation & Benchmarking

### Practical Benchmark Suite

1. Golden Q&A set
- 30-50 curated questions across all modules.
- Includes factual, conceptual, and troubleshooting prompts.

2. Hallucination tracking
- Manual scoring sheet per response: grounded / uncertain / hallucinated.

3. Retrieval recall@k
- Measure if supporting chunk exists in top-k retrieval for golden queries.

4. Prompt regression tests
- Fixed prompts run before each demo lock.
- Detect response drift after prompt or model changes.

5. Versioned embeddings
- Record embedding model ID + chunking version.
- Reindex only on content or embedding version change.

### Acceptance Thresholds (Hackathon Realistic)

- Recall@10 >= 0.80 on golden set.
- Hallucination <= 10% on golden set.
- Mean response latency <= 3s in demo environment.

---

## Content Lifecycle Workflow

### Lifecycle (Hackathon)

AI Editor Draft -> Domain Expert Review -> Embed -> Publish

### Roles and Responsibilities

- AI Editor: generates first drafts from curriculum outline, improves clarity, structure, and consistency using Claude Code + Spec-Kit Plus.
- Domain Expert: validates technical correctness (ROS 2 commands, API signatures, simulation workflows).
- Integration Owner: handles embedding ingestion and link integrity.
- Release Owner: publishes and confirms UI + chat behavior.

### Exit Criteria per Stage

- AI Editor Draft: complete chapter with learning objectives, ≥800 prose words, 3+ titled sections, ≥1 code example, chapter summary.
- Domain Expert Review: technical sign-off complete; corrections committed.
- Embed: content indexed and retrievable in Qdrant.
- Publish: chapter visible at published URL and chat-tested.

---

## 90-Second Demo Playbook

### Visual Sequence and Script

#### 0-15 sec: Landing Page + Mission

User actions:
- Open homepage.
- Scroll to one featured module card.

Say:
- "This is an AI-native Physical AI textbook built in Docusaurus with integrated tutoring."

Show:
- Clean landing page, chapter navigation, mission statement.

#### 15-35 sec: RAG + Selected Text

User actions:
- Open a chapter section.
- Highlight one paragraph.
- Ask: "Explain this for a beginner and cite the source section."

Say:
- "The chatbot grounds answers in selected text and chapter retrieval, then cites sources."

Show:
- Selected text indicator, chat streaming response, citation links.

#### 35-55 sec: Bonus Feature 1 (e.g., Quiz Agent)

User actions:
- Request a quiz on the current chapter.

Say:
- "The quiz agent generates grounded multiple-choice questions from chapter content."

Show:
- Quiz output with questions, options, and explanations.

#### 55-70 sec: Bonus Feature 2 (e.g., Personalization)

User actions:
- Open profile preset (e.g., Software Engineer path).
- Click `Personalize` on the same section.

Say:
- "The same content adapts to the learner profile while preserving technical correctness."

Show:
- Before/after personalized block in-place.

#### 70-90 sec: GitHub + Architecture + CTA

User actions:
- Show repository.
- Show one architecture diagram.
- Return to app.

Say:
- "Built with Docusaurus, FastAPI, OpenAI Agents SDK, Qdrant, and Neon. Ready to scale beyond hackathon."

Show:
- README, architecture snapshot, live app URL.

### What Not to Show

- Long terminal sessions.
- Unstable experimental features.
- Lengthy environment setup.
- Any flow that risks authentication failure in demo time.
- Any screen that has secrets, keys, or admin consoles.

### Demo Hard Rules

- One narrator only.
- One backup browser tab preloaded.
- Total runtime <= 90 seconds.
- Rehearsed minimum 5 times with timer.

### Demo Contingency Runbook

#### Failure: Chat API unavailable

Action:
- Switch to preloaded successful chat session screenshot/video clip.

Say:
- \"Live API is under temporary load; this capture shows the same deployed flow from rehearsal with citations.\"

Visual:
- Citation-backed response with selected-text indicator.

#### Failure: Auth flow breaks

Action:
- Use pre-authenticated backup browser profile tab.

Say:
- \"Using the backup signed-in session to keep timing and show protected features.\"

Visual:
- Personalization button enabled and profile preset visible.

#### Failure: Translation timeout

Action:
- Show pre-generated Urdu translation artifact from same section.

Say:
- \"This is the same section translation output generated from the deployed translate endpoint.\"

Visual:
- Before/after translated block with preserved formatting.

#### Failure: Deployment instability

Action:
- Move to fallback static demo page with architecture + recorded walkthrough.

Say:
- \"Fallback mode preserves the full evaluated flow and proof links in the repository.\"

Visual:
- Timeline, architecture, proof links, and recorded end-to-end run.

---

## Submission Checklist

- Public GitHub repository with README and demo link.
- 90-second video (5 segments):
  - 0-15 sec: homepage + module + chapter navigation
  - 15-35 sec: RAG chatbot + selected-text Q&A with citations
  - 35-55 sec: bonus feature 1 (e.g., quiz agent)
  - 55-70 sec: bonus feature 2 (e.g., personalization)
  - 70-90 sec: GitHub repo + architecture diagram + live app URL
- Recording tool: YouTube (unlisted) or Loom.
- Submission form completed before deadline.

---

## Winning Strategy

- Win condition: Base complete + two excellent bonuses + crisp demo narrative.
- Moat targets:
  - 200 points = top 20% candidate profile
  - 250 points = top 10% candidate profile
- Avoid:
  - Attempting all bonuses simultaneously.
  - Demo exceeding 90 seconds.
  - Last-minute deployment changes.

---

## Governance

### Decision Protocol

- Product decisions: hackathon lead.
- Technical decisions: architecture lead.
- Content correctness: domain reviewer.
- Final demo sign-off: team lead and presenter.

### Change Control

- Any scope increase requires explicit impact on demo timeline.
- Breaking API changes freeze 48 hours before final recording.
- New features after freeze only if they reduce demo risk.

### Versioning

- Document version: 2.1
- API version prefix: `/api/v1`
- Ratified date: 2026-02-15
- Last amended date: 2026-02-15

---

## Business & Ecosystem Vision

- Freemium model: open core chapters, premium guided paths.
- Certification pathways for Physical AI fundamentals.
- Institutional licensing for schools and training programs.
- Sponsored robotics labs and partner-funded challenge modules.
- Expansion roadmap to O/A Level and adjacent STEM AI-native textbooks.

---

## Appendix

### Appendix A: Extended Technical Snippets

Below is the embedded technical snippet archive previously stored as a separate file.

## Moved Code Snippets Archive

This file contains content moved from `constitution.md` lines 2800-5200.

    healthCheckPath: /health
    numInstances: 3

    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: textbook-db
          property: connectionString

      - key: QDRANT_URL
        value: https://your-cluster.qdrant.io

      - key: QDRANT_API_KEY
        sync: false

databases:
  - name: textbook-db
    databaseName: textbook
    plan: standard

  - name: redis
    plan: standard
```

#### Fly.io Configuration (fly.toml):
```toml
app = "physical-ai-textbook"
primary_region = "ord"

[build]
  dockerfile = "Dockerfile"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 1
  processes = ["app"]

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 1024

[env]
  PORT = "8000"
  APP_ENV = "production"
  DEBUG = "false"

[[statics]]
  guest_path = "/app/static"
  url_prefix = "/static/"
```

### Environment Configuration

**.env.example**:
```bash
# Application
APP_ENV=production
DEBUG=false
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# Redis
REDIS_URL=redis://host:6379
REDIS_CACHE_TTL=3600

# Qdrant
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION=physical_ai_textbook

# OpenAI Agents SDK
COHERE_API_KEY=your-cohere-api-key
COHERE_MODEL=command-r-plus

# Better Auth
AUTH_SECRET=your-auth-secret
AUTH_URL=https://your-domain.com
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# Monitoring
SENTRY_DSN=your-sentry-dsn
SENTRY_ENVIRONMENT=production

# CORS
CORS_ORIGINS=https://yourusername.github.io,https://your-domain.com

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
```

## 4. Database Setup

### Neon Postgres Configuration

**Initialization Script** (init_db.py):
```python
import asyncpg
import asyncio
from pathlib import Path

async def init_database(connection_string: str):
    """Initialize database with schema"""

    # Connect to database
    conn = await asyncpg.connect(connection_string)

    try:
        # Read schema file
        schema_path = Path(__file__).parent / "schema.sql"
        schema_sql = schema_path.read_text()

        # Execute schema
        await conn.execute(schema_sql)

        print("✓ Database schema created")

        # Create indexes
        indexes_path = Path(__file__).parent / "indexes.sql"
        indexes_sql = indexes_path.read_text()
        await conn.execute(indexes_sql)

        print("✓ Indexes created")

        # Seed initial data
        seed_path = Path(__file__).parent / "seed.sql"
        if seed_path.exists():
            seed_sql = seed_path.read_text()
            await conn.execute(seed_sql)
            print("✓ Initial data seeded")

    finally:
        await conn.close()

if __name__ == "__main__":
    import os
    db_url = os.getenv("DATABASE_URL")
    asyncio.run(init_database(db_url))
```

**Migration Script**:
```python
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '001'
down_revision = None

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255)),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('email')
    )

    # Create user_profiles table
    op.create_table(
        'user_profiles',
        sa.Column('profile_id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('python_level', sa.String(20)),
        sa.Column('ros_experience', sa.Boolean(), default=False),
        sa.Column('ai_knowledge', sa.String(20)),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('profile_id')
    )

    # Create chapter_progress table
    op.create_table(
        'chapter_progress',
        sa.Column('progress_id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('chapter_id', sa.String(50), nullable=False),
        sa.Column('module_number', sa.Integer),
        sa.Column('completion_percentage', sa.DECIMAL(5, 2), default=0.00),
        sa.Column('time_spent_seconds', sa.Integer, default=0),
        sa.Column('last_position', sa.String(100)),
        sa.Column('status', sa.String(20)),
        sa.Column('first_accessed', sa.DateTime()),
        sa.Column('last_accessed', sa.DateTime()),
        sa.Column('completed_at', sa.DateTime()),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('progress_id'),
        sa.UniqueConstraint('user_id', 'chapter_id')
    )

    # Create quiz_results table
    op.create_table(
        'quiz_results',
        sa.Column('result_id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('quiz_id', sa.String(50), nullable=False),
        sa.Column('chapter_id', sa.String(50)),
        sa.Column('score', sa.DECIMAL(5, 2)),
        sa.Column('max_score', sa.DECIMAL(5, 2)),
        sa.Column('percentage', sa.DECIMAL(5, 2)),
        sa.Column('attempt_number', sa.Integer),
        sa.Column('time_taken_seconds', sa.Integer),
        sa.Column('submitted_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('answers', sa.JSON),
        sa.Column('feedback', sa.JSON),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('result_id')
    )

    # Create chat_sessions table
    op.create_table(
        'chat_sessions',
        sa.Column('session_id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('chapter_id', sa.String(50)),
        sa.Column('started_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('last_message_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('message_count', sa.Integer, default=0),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('session_id')
    )

    # Create chat_messages table
    op.create_table(
        'chat_messages',
        sa.Column('message_id', sa.UUID(), nullable=False),
        sa.Column('session_id', sa.UUID(), nullable=False),
        sa.Column('role', sa.String(20)),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('selected_text', sa.Text),
        sa.Column('context_sources', sa.JSON),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('tokens_used', sa.Integer),
        sa.Column('response_time_ms', sa.Integer),
        sa.Column('user_rating', sa.Integer),
        sa.Column('user_feedback', sa.Text),
        sa.ForeignKeyConstraint(['session_id'], ['chat_sessions.session_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('message_id')
    )

def downgrade():
    op.drop_table('chat_messages')
    op.drop_table('chat_sessions')
    op.drop_table('quiz_results')
    op.drop_table('chapter_progress')
    op.drop_table('user_profiles')
    op.drop_table('users')
```

### Connection Pooling
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

## 5. Monitoring & Observability

### Application Monitoring Setup
```python
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
import logging

# Initialize Sentry
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[
        FastApiIntegration(),
        SqlalchemyIntegration(),
    ],
    traces_sample_rate=0.1,
    profiles_sample_rate=0.1,
    environment=os.getenv("APP_ENV", "development")
)

# Initialize FastAPI
app = FastAPI(
    title="Physical AI Textbook API",
    version="1.0.0"
)

# Add Prometheus metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# Structured logging
logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)
```

### Health Check Endpoints
```python
from fastapi import APIRouter, HTTPException
from sqlalchemy import text
import redis
import os

router = APIRouter()

@router.get("/health")
async def health_check():
    """Comprehensive health check"""
    checks = {
        "api": "healthy",
        "database": await check_database(),
        "redis": await check_redis(),
        "qdrant": await check_qdrant()
    }

    if any(status != "healthy" for status in checks.values()):
        raise HTTPException(status_code=503, detail=checks)

    return checks

async def check_database():
    """Check database connectivity"""
    try:
        async with get_db() as db:
            await db.execute(text("SELECT 1"))
        return "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return "unhealthy"

async def check_redis():
    """Check Redis connectivity"""
    try:
        redis_client = redis.from_url(os.getenv("REDIS_URL"))
        redis_client.ping()
        return "healthy"
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        return "unhealthy"

async def check_qdrant():
    """Check Qdrant connectivity"""
    try:
        from qdrant_client import QdrantClient
        client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        client.get_collections()
        return "healthy"
    except Exception as e:
        logger.error(f"Qdrant health check failed: {e}")
        return "unhealthy"
```

### Logging Configuration
```python
import logging
import sys
from pythonjsonlogger import jsonlogger
from datetime import datetime

def setup_logging():
    # Create custom formatter
    json_formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S.%fZ'
    )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Create handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(json_formatter)
    
    # Add handler to root logger
    root_logger.addHandler(handler)
    
    # Suppress noisy loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

# Call this function during application startup
setup_logging()
```

### Metrics Collection
```python
from prometheus_client import Counter, Histogram, Gauge

# Custom metrics
rag_query_total = Counter(
    'rag_query_total',
    'Total RAG queries',
    ['chapter', 'query_type']
)

rag_query_duration = Histogram(
    'rag_query_duration_seconds',
    'RAG query duration',
    ['chapter']
)

active_users = Gauge(
    'active_users',
    'Number of active users'
)

embedding_cache_hits = Counter(
    'embedding_cache_hits_total',
    'Embedding cache hits'
)

embedding_cache_misses = Counter(
    'embedding_cache_misses_total',
    'Embedding cache misses'
)

# Usage in code
@app.post("/api/v1/chat/query")
async def chat_query(query: ChatQuery):
    start_time = time.time()

    # Track query
    rag_query_total.labels(
        chapter=query.chapter_context or 'general',
        query_type=classify_query(query.query)
    ).inc()

    try:
        result = await process_query(query)

        # Track duration
        duration = time.time() - start_time
        rag_query_duration.labels(
            chapter=query.chapter_context or 'general'
        ).observe(duration)

        return result
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise
```

## 6. Security Implementation

### API Security Code
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
import os

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/v1/chat/query")
@limiter.limit("60/minute")
async def chat_query(request: Request, query: ChatQuery):
    # ... implementation

# CORS Configuration
allowed_origins = os.getenv("CORS_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count"],
    max_age=600,
)

# Input Validation
class ChatQuery(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    chapter_context: Optional[str] = Field(None, max_length=50)
    selected_text: Optional[str] = Field(None, max_length=5000)

    @validator('query')
    def validate_query(cls, v):
        # Sanitize input
        if len(v.strip()) == 0:
            raise ValueError("Query cannot be empty")

        # Check for injection attempts
        dangerous_patterns = ['<script>', 'DROP TABLE', 'DELETE FROM']
        if any(pattern in v.upper() for pattern in dangerous_patterns):
            raise ValueError("Invalid query content")

        return v.strip()
```

### Data Encryption
```python
from cryptography.fernet import Fernet
import base64
import os

class DataEncryption:
    def __init__(self, key: bytes):
        self.fernet = Fernet(key)

    def encrypt(self, data: str) -> str:
        """Encrypt sensitive data"""
        encrypted = self.fernet.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        decoded = base64.b64decode(encrypted_data.encode())
        decrypted = self.fernet.decrypt(decoded)
        return decrypted.decode()

# Usage
encryption_key = os.getenv("ENCRYPTION_KEY").encode()
crypto = DataEncryption(encryption_key)

# Encrypt PII before storing
user.email_encrypted = crypto.encrypt(user.email)
```

## 7. Backup & Disaster Recovery

### Backup Scripts
```bash
#!/bin/bash

# Backup configuration
BACK_UP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACK_UP_FILE="textbook_db_${DATE}.sql.gz"

# Create backup
pg_dump $DATABASE_URL | gzip > "${BACK_UP_DIR}/${BACK_UP_FILE}"

# Upload to S3
aws s3 cp "${BACK_UP_DIR}/${BACK_UP_FILE}" s3://your-backup-bucket/database/

# Keep only last 30 days locally
find ${BACK_UP_DIR} -name "textbook_db_*.sql.gz" -mtime +30 -delete

echo "Backup completed: ${BACK_UP_FILE}"
```

### Backup Cron Job
```
0 2 * * * /scripts/backup_database.sh
```

### Qdrant Backups
```python
import asyncio
from qdrant_client import QdrantClient
from datetime import datetime

async def backup_qdrant():
    """Backup Qdrant collection"""
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    # Create snapshot
    snapshot_info = client.create_snapshot(
        collection_name="physical_ai_textbook"
    )

    # Download snapshot
    snapshot_data = client.download_snapshot(
        collection_name="physical_ai_textbook",
        snapshot_name=snapshot_info.name
    )

    # Save to file
    backup_path = f"/backups/qdrant_{datetime.now():%Y%m%d_%H%M%S}.snapshot"
    with open(backup_path, 'wb') as f:
        f.write(snapshot_data)

    print(f"Qdrant backup created: {backup_path}")
```

### Recovery Procedures
```bash
#!/bin/bash

# Database recovery script
RESTORE_FILE=$1

if [ -z "$RESTORE_FILE" ]; then
    echo "Usage: $0 <backup_file>"
    exit 1
fi

if [ ! -f "$RESTORE_FILE" ]; then
    echo "Backup file not found: $RESTORE_FILE"
    exit 1
fi

echo "Restoring database from $RESTORE_FILE..."
gunzip -c "$RESTORE_FILE" | psql $DATABASE_URL

if [ $? -eq 0 ]; then
    echo "Database restored successfully!"
else
    echo "Database restore failed!"
    exit 1
fi
```

## 8. Performance Optimization

### Caching Implementation
```python
from functools import wraps
import pickle

def cache_response(ttl: int = 3600):
    """Decorator to cache responses"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"

            # Check cache
            cached = redis_client.get(cache_key)
            if cached:
                return pickle.loads(cached)

            # Execute function
            result = await func(*args, **kwargs)

            # Cache result
            redis_client.setex(
                cache_key,
                ttl,
                pickle.dumps(result)
            )

            return result
        return wrapper
    return decorator

# Usage
@cache_response(ttl=1800)
async def get_chapter_content(chapter_id: str):
    # Expensive operation
    return await fetch_from_database(chapter_id)
```

### Database Optimization
```sql
-- Create indexes for common queries
CREATE INDEX idx_chapter_progress_user_chapter
ON chapter_progress(user_id, chapter_id);

CREATE INDEX idx_chat_messages_session_created
ON chat_messages(session_id, created_at DESC);

CREATE INDEX idx_quiz_results_user_submitted
ON quiz_results(user_id, submitted_at DESC);

-- Partial indexes for active sessions
CREATE INDEX idx_chat_sessions_active
ON chat_sessions(user_id, last_message_at DESC)
WHERE is_active = true;

-- Full-text search index
CREATE INDEX idx_content_search
ON content USING GIN(to_tsvector('english', content_text));
```

## 9. CI/CD Pipelines

### Testing Pipeline
**.github/workflows/test.yml**:
```yaml
name: Run Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio pytest-cov

      - name: Run linting
        run: |
          pip install flake8 black isort mypy
          flake8 app/
          black --check app/
          isort --check app/
          mypy app/

      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost/test_db
          REDIS_URL: redis://localhost:6379
        run: |
          pytest --cov=app --cov-report=xml tests/

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

### Deployment Automation
**.github/workflows/deploy-production.yml**:
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ secrets.REGISTRY_URL }}
          username: ${{ secrets.REGISTRY_USERNAME }}
          password: ${{ secrets.REGISTRY_PASSWORD }}

      - name: Build and Push Docker Image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ secrets.REGISTRY_URL }}/physical-ai-textbook:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Deploy to Platform
        run: |
          # Deploy using platform-specific CLI
          # Example for Railway:
          # railway up --service physical-ai-api --environment production
          
          # Example for Render:
          # curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}
          
          # Example for Fly.io:
          # flyctl deploy --image ${{ secrets.REGISTRY_URL }}/physical-ai-textbook:${{ github.sha }}
```


### Source: docs/education/educational-framework.md

# Instructional Design Document

> **Note**: This is a companion document to the Project Constitution. For project 
> governance, scope, and objectives, see [constitution.md](../../constitution.md).
> 
> **Related Guides**: 
> - [Content Style Guide](../process/content-style-guide.md) - For writing standards
> - [Quality Assurance Checklist](../process/quality-assurance-checklist.md) - For quality standards

## 1. Teaching Philosophy

### Constructivist Approach
Physical AI education builds on students' existing knowledge of software AI and programming, progressively introducing physical constraints and embodied intelligence concepts. Learning occurs through active construction of understanding rather than passive reception.

### Deliberate Practice Framework
- **Focused Practice**: Each chapter targets specific skills
- **Immediate Feedback**: AI chatbot provides instant clarification
- **Gradual Complexity**: Scaffolded learning from simple to complex
- **Reflection**: End-of-chapter summaries encourage metacognition

### Kolb's Experiential Learning Cycle
1. **Concrete Experience**: Hands-on simulation exercises
2. **Reflective Observation**: Analysis of what happened and why
3. **Abstract Conceptualization**: Theory connecting to practice
4. **Active Experimentation**: Apply learnings to new scenarios

## 2. Learning Objectives Framework (Bloom's Taxonomy)

### Remember (Weeks 1-2)
- Define key concepts: Physical AI, embodied intelligence, sensor types
- List components of robotic systems
- Identify safety considerations

### Understand (Weeks 3-5)
- Explain ROS 2 architecture and communication patterns
- Describe URDF structure for robot modeling
- Interpret sensor data and its limitations

### Apply (Weeks 6-7)
- Implement robot simulations in Gazebo
- Configure sensor models with appropriate parameters
- Use launch files to start complex systems

### Analyze (Weeks 8-10)
- Compare different SLAM algorithms
- Evaluate trade-offs in sensor selection
- Debug multi-component robot systems

### Evaluate (Weeks 11-12)
- Assess humanoid robot designs
- Critique grasping strategies for different objects
- Justify control algorithm choices

### Create (Weeks 13)
- Design complete autonomous robot system
- Synthesize multiple technologies (voice, vision, navigation, manipulation)
- Innovate solutions to novel problems

## 3. Content Development Guidelines

### Cognitive Load Management

**Intrinsic Load (Content Complexity)**:
- Start with familiar concepts (Python, AI) before introducing robotics
- Chunk information into digestible sections (5-7 concepts per chapter)
- Use progressive disclosure: Basic → Intermediate → Advanced

**Extraneous Load (Presentation)**:
- Clean, consistent formatting
- Diagrams follow same visual language
- Code examples with clear structure
- Minimal distractions in interface

**Germane Load (Schema Building)**:
- Explicit connections between chapters
- Analogies to familiar concepts
- Visual concept maps showing relationships
- Pattern recognition exercises

### Mayer's Multimedia Learning Principles

1. **Multimedia Principle**: Use words + pictures (not just words)
   - Every complex concept has a diagram
   - Architecture explanations include visual representations
   - Code examples paired with flowcharts

2. **Contiguity Principle**: Related content close together
   - Diagrams adjacent to explanations
   - Code comments inline, not separate
   - Examples immediately after theory

3. **Modality Principle**: Graphics + narration better than graphics + text
   - Video tutorials for complex procedures
   - AI chatbot can "explain verbally"
   - Audio feedback for interactive elements

4. **Redundancy Principle**: Graphics + narration better than graphics + narration + text
   - Avoid reading text that appears on screen
   - Diagrams annotated, not duplicated in text
   - Code comments complement, not repeat code

5. **OpenAI Agents SDKnce Principle**: Exclude extraneous material
   - Stay focused on learning objectives
   - Remove "interesting but irrelevant" tangents
   - Keep examples directly related to concepts

6. **Signaling Principle**: Highlight essential content
   - Bold key terms on first use
   - Callout boxes for critical information
   - Icons to indicate type of content (concept, code, exercise)

7. **Segmenting Principle**: Break into learner-controlled segments
   - Chapters divided into logical sections
   - Expandable code examples
   - Progressive exercises (basic → advanced)

8. **Pre-training Principle**: Introduce components before the process
   - Key terms defined before complex explanations
   - Component overview before system architecture
   - Prerequisites clearly stated

9. **Personalization Principle**: Conversational style
   - Use "you" and "we" language
   - Friendly, engaging tone
   - Questions to provoke thought

## 4. Assessment Strategies

### Formative Assessment (Ongoing)

**Knowledge Checks (Every Section)**:
- Multiple choice: Quick comprehension verification
- Short answer: Explain in own words
- Code reading: Predict output or find bugs

**Interactive Quizzes (Every Chapter)**:
- Auto-graded for immediate feedback
- Adaptive difficulty based on performance
- Hints available after first attempt
- Explanations for all answers

**Progress Tracking**:
- Chapter completion percentage
- Time spent on each section
- Quiz scores over time
- Chatbot interaction frequency

### Summative Assessment

**Module Projects (End of Modules 1-3)**:
- Small, focused projects demonstrating mastery
- Graded on functionality, code quality, documentation
- Peer review component
- Rubric provided in advance

**Capstone Project (Week 13)**:
- Comprehensive integration project
- Multiple evaluation criteria:
  - Technical: Does it work? How well?
  - Documentation: Clear README, comments, report
  - Presentation: Effective communication
  - Innovation: Creative problem-solving

### Assessment Rubrics

**Code Quality Rubric**:
| Criterion | Excellent (4) | Good (3) | Satisfactory (2) | Needs Work (1) |
|-----------|---------------|----------|------------------|----------------|
| Functionality | Works perfectly, handles edge cases | Works correctly for normal inputs | Works with minor issues | Significant bugs |
| Organization | Modular, well-structured | Mostly organized | Some structure | Disorganized |
| Documentation | Comprehensive comments and README | Good comments | Minimal comments | No documentation |
| Style | Follows PEP 8, consistent | Mostly consistent | Inconsistent | Poor style |

**Project Report Rubric**:
| Criterion | Excellent (4) | Good (3) | Satisfactory (2) | Needs Work (1) |
|-----------|---------------|----------|------------------|----------------|
| Problem Statement | Clear, compelling, well-motivated | Clear and appropriate | Present but unclear | Missing or unclear |
| Technical Depth | Thorough explanation with details | Good explanation | Superficial | Lacking substance |
| Results | Comprehensive with metrics | Good results shown | Results present | Missing results |
| Analysis | Deep insights and reflection | Some analysis | Minimal analysis | No analysis |
| Presentation | Professional, clear, engaging | Clear presentation | Acceptable | Poor quality |

## 5. Differentiation Strategies

### For Beginners
- More scaffolding in exercises
- Additional worked examples
- Slower pacing in tutorials
- Glossary of terms always accessible
- "Explain like I'm 5" AI mode

### For Advanced Learners
- Optional advanced sections
- Research paper references
- Open-ended challenges
- Optimization problems
- Contribution opportunities (extend course)

### For Different Hardware Access
- **No GPU**: Cloud alternatives clearly explained
- **No Robot**: Simulation-only path with equal rigor
- **Basic Setup**: Modifications for lower-spec hardware
- **Full Setup**: Additional hardware-specific projects

## 6. Engagement Strategies

### Motivation

**Relevance**: Connect every topic to real applications
- Module 1: "This is how Boston Dynamics robots communicate"
- Module 2: "Tesla uses simulation to train Optimus"
- Module 3: "Amazon robots use VSLAM for warehouse navigation"
- Module 4: "This is the tech behind ChatGPT-controlled robots"

**Autonomy**: Student choice where appropriate
- Choose capstone project scenario
- Select between alternative implementations
- Personalize learning path based on background

**Mastery**: Clear progress indicators
- Badges for chapter completion
- Skill trees showing unlocked capabilities
- Leaderboard for optional challenges (opt-in)

**Purpose**: The "why" is always clear
- Chapter introductions explain importance
- Case studies show real-world impact
- Career pathways highlighted

### Active Learning Techniques

**Think-Pair-Share**:
- Chatbot poses question
- Student thinks independently
- Student discusses with peer (if in classroom)
- Student shares with chatbot for feedback

**Predict-Observe-Explain**:
- Predict: What will happen when we run this code?
- Observe: Run it and see actual result
- Explain: Why did it behave that way?

**Worked Examples with Self-Explanation**:
- Provide partially completed code
- Student explains each completed line
- Student completes remaining code
- Chatbot validates explanations

**Debugging Exercises**:
- Provide buggy code
- Student must find and fix errors
- Multiple bugs of increasing subtlety
- Chatbot provides hints if stuck

## 7. Universal Design for Learning (UDL)

### Multiple Means of Representation
- Text explanations
- Video demonstrations
- Interactive simulations
- Audio narration option
- Diagrams and infographics

### Multiple Means of Engagement
- Different difficulty levels
- Various project options
- Gamification elements (optional)
- Real-world connections
- Community features (forums, showcases)

### Multiple Means of Action and Expression
- Written reports
- Video presentations
- Code portfolios
- Interactive demos
- Peer teaching opportunities

## 8. Accessibility Features

### Visual
- High contrast mode
- Adjustable text size
- Alt text for all images
- Color-blind friendly palette
- No information conveyed by color alone

### Auditory
- Captions for all videos
- Transcripts available
- Visual indicators for audio cues

### Motor
- Keyboard navigation
- No time-pressured tasks
- Click targets adequately sized
- No double-click requirements

### Cognitive
- Clear, simple language
- Consistent navigation
- Progress saving
- No information overload
- Distraction-free reading mode

## 9. Feedback Mechanisms

### Automated Feedback (Immediate)

**Code Execution**:
- Run code in browser
- Show output and errors
- Suggest common fixes
- Link to relevant documentation

**Quiz Questions**:
- Instant correct/incorrect
- Explanation for each answer
- Link to relevant content section
- Option to retake

**Chatbot Interactions**:
- Acknowledge questions
- Provide tailored explanations
- Suggest related topics
- Encourage follow-up questions

### AI Tutor Feedback (On-Demand)

**Code Review**:
- "Can you review my code?"
- Chatbot analyzes for bugs, style, efficiency
- Provides suggestions, not solutions
- Encourages good practices

**Concept Clarification**:
- "I don't understand X"
- Chatbot provides alternative explanation
- Uses analogies or examples
- Checks understanding with follow-up question

**Debugging Assistance**:
- "Why isn't this working?"
- Chatbot helps troubleshoot systematically
- Teaches debugging process
- Doesn't just give answer

### Instructor Feedback (Periodic)

**Project Submissions**:
- Detailed rubric-based feedback
- Specific suggestions for improvement
- Recognition of strengths
- Guidance for next steps

**Progress Check-ins**:
- Weekly or bi-weekly
- Identify struggling students
- Celebrate achievements
- Adjust pacing if needed

---

*This Instructional Design Document contains all the pedagogical content that was originally in the constitution, organized by category for easy reference during curriculum development and instruction.*


### Source: docs/process/content-style-guide.md

# Content Style Guide

> **Note**: This is a companion document to the Project Constitution. For project 
> governance, scope, and objectives, see [constitution.md](../../constitution.md).
> 
> **Related Guides**: 
> - [Educational Framework](../education/educational-framework.md) - For pedagogical approaches
> - [Quality Assurance Checklist](../process/quality-assurance-checklist.md) - For quality standards

## 1. Writing Standards

### Clarity and Accessibility
- Write for students with AI fundamentals but new to robotics
- Define technical terms on first use
- Use progressive disclosure (simple → complex)

### Practical Focus
- Include hands-on examples for every concept
- Provide code snippets with explanations
- Link theory to real-world applications

### Visual Learning
- Diagrams for architecture and workflows
- Screenshots for software setup
- Videos for demonstrations (where applicable)
- Interactive simulations (where possible)

### AI-Native Approach
- Embed chatbot assistance throughout
- Provide alternative explanations via AI
- Enable "explain like I'm 5" mode
- Support code debugging through chat

## 2. Chapter Structure Template

```markdown
# Chapter Title

## Learning Objectives
- Clear, measurable outcomes

## Prerequisites
- Required knowledge/setup

## Introduction
- Context and motivation
- Real-world relevance

## Core Concepts
- Detailed explanations
- Code examples
- Diagrams/visuals

## Hands-On Practice
- Step-by-step tutorials
- Common pitfalls and solutions

## Assessment
- Knowledge check questions
- Practical exercises
- Project ideas

## Further Resources
- Official documentation links
- Research papers
- Community resources

## Summary
- Key takeaways
- Connection to next chapter
```

## 3. Code Formatting

### Language-Specific Conventions
- **Python**: Follow PEP 8 style guide
- **JavaScript/TypeScript**: Use consistent indentation (2 spaces)
- **Shell/Bash**: Use consistent quoting and spacing
- **Configuration Files**: Follow language-specific best practices

### Comment Requirements
- Explain the "why" not just the "what"
- Use inline comments sparingly but strategically
- Include docstrings for functions and classes
- Comment complex algorithms thoroughly
- Update comments when code changes

### Example Quality Standards
- Code examples must be complete and functional
- Include at least one explicit error-path example for snippets that perform I/O, parsing, or network calls
- Use meaningful variable and function names
- Follow the principle of least surprise
- Include comments explaining non-obvious parts
- Test examples in the target environment
- Keep examples focused on the concept being taught

## 4. Media Guidelines

### Image Requirements
- **Format**: New raster images must be WebP; PNG/JPEG allowed only for compatibility or transparency constraints
- **Size**: New images must be <= 200KB; if larger, document reason in PR and provide compressed variant
- **Alt Text**: Provide descriptive alt text for all images
- **Resolution**: Minimum 72 DPI for screen display
- **Dimensions**: Maintain aspect ratio, avoid distortion
- **File Names**: Use descriptive, lowercase names with hyphens

### Video Specifications
- **Format**: MP4 with H.264 codec
- **Resolution**: Minimum 720p, 1080p preferred
- **Frame Rate**: 30fps standard
- **Audio**: Clear, noise-free audio with consistent volume
- **Captions**: Provide closed captions for accessibility
- **Length**: Keep each instructional video <= 5 minutes (demo/overview clips may be <= 10 minutes)
- **Thumbnails**: Provide relevant thumbnail image

### Diagram Standards
- **Style**: Consistent visual language throughout
- **Colors**: Use color-blind friendly palettes
- **Labels**: Diagram label text must remain readable at 100% zoom with minimum equivalent size of 14px in exported assets
- **Arrows/Connectors**: Use consistently to show relationships
- **Legends**: Include legends when necessary
- **Export**: High-resolution PNG or SVG format

## 5. Markdown Formatting

### Header Hierarchy
- Use `#` for main chapter titles
- Use `##` for major sections
- Use `###` for subsections
- Use `####` for sub-subsections (sparingly)
- Never skip header levels (don't go from `##` to `####`)

### List Formatting
- Use `-` for unordered lists
- Use `1.`, `2.`, `3.` for ordered lists
- Maintain consistent indentation (2 spaces)
- Use blank lines appropriately around lists
- For nested lists, indent with 2 spaces per level

### Link Conventions
- Use descriptive link text rather than URLs
- Place links immediately after the relevant text
- Use relative links for internal references
- Use absolute URLs for external references
- Verify all links are functional before publishing

## 6. Accessibility Requirements

### Alt Text Guidelines
- Provide meaningful alt text for all images
- Describe the content and function of the image
- Keep alt text concise but informative
- For decorative images, use empty alt text (`alt=""`)
- For complex diagrams, provide extended descriptions

### Color Usage
- Maintain sufficient contrast ratios (minimum 4.5:1 for normal text)
- Don't rely solely on color to convey information
- Use color-blind friendly palettes
- Test color combinations with accessibility tools
- Provide text alternatives for color-coded information

### Font and Sizing
- Use web-safe fonts or properly licensed web fonts
- Maintain readable font sizes (minimum 16px for body text)
- Use relative units (em, rem) for scalability
- Ensure text can be resized up to 200% without loss of functionality
- Maintain proper line height for readability (1.4-1.6)

---

*This Content Style Guide serves as the definitive reference for all content creators contributing to the Physical AI & Humanoid Robotics Textbook project.*


### Source: docs/process/contributor-handbook.md

# Contributor Handbook

> **Note**: This is a companion document to the Project Constitution. For project 
> governance, scope, and objectives, see [constitution.md](../../constitution.md).
> 
> **Related Guides**: 
> - [Content Style Guide](../process/content-style-guide.md) - For writing standards
> - [Technical Implementation Guide](../architecture/technical-implementation-guide.md) - For development practices
> - [Quality Assurance Checklist](../process/quality-assurance-checklist.md) - For quality standards

## 1. Getting Started

### Prerequisites
- Git installed and configured
- Node.js v18+ for frontend development
- Python 3.11+ for backend development
- Docker and Docker Compose for containerization
- An API key for OpenAI Agents SDK for the RAG functionality

### Initial Setup
```bash
# Clone the repository
git clone <repository-url>
cd <project-directory>

# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your actual API keys and configuration
```

### Development Environment
- Use a modern IDE with appropriate plugins for Python and JavaScript
- Configure your editor to use 2-space indentation for JavaScript/TypeScript
- Configure your editor to use 4-space indentation for Python
- Enable prettier/eslint for JavaScript/TypeScript
- Enable black/isort for Python

## 2. Code Style Guidelines

### Python Style
- Follow PEP 8 style guide
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions and methods <= 50 lines by default; any function > 80 lines requires a refactor note in review
- Use meaningful variable and function names

### JavaScript/TypeScript Style
- Use 2-space indentation
- Use camelCase for variables and functions
- Use PascalCase for constructors and components
- Write JSDoc for exported functions
- Keep functions <= 30 lines by default; any function > 60 lines requires a refactor note in review
- Use meaningful variable and function names

### Commit Message Guidelines
- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests after the description
- Consider starting the commit message with an applicable emoji:
  - 🎉 `:tada:` when adding a new feature
  - 🐛 `:bug:` when fixing a bug
  - 📝 `:memo:` when writing docs
  - 🚀 `:rocket:` when improving performance
  - 🔧 `:wrench:` when changing configuration
  - 💄 `:lipstick:` when improving UI

## 3. Contribution Process

### Creating a Branch
```bash
# Create a branch for your feature or fix
git checkout -b feature/my-new-feature
# or
git checkout -b fix/issue-description
```

### Making Changes
- Write clear, well-documented code
- Follow the style guidelines outlined in this document
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass before submitting

### Testing
```bash
# Run Python tests
cd backend
pytest

# Run JavaScript tests
cd frontend
npm test

# Run linting
cd backend
flake8 .
black --check .
isort --check-only .

cd frontend
npm run lint
npm run typecheck
```

### Submitting Changes
```bash
# Commit your changes
git add .
git commit -m "feat: add new feature"

# Push to your branch
git push origin feature/my-new-feature

# Create a pull request
# Go to the repository on GitHub and create a pull request
```

## 4. Pull Request Guidelines

### Before Submitting
- Ensure all tests pass
- Verify code follows style guidelines
- Update documentation for any public behavior, API contract, config, or UX change
- Add or update tests for every behavior change, or document a `no-test-needed` rationale in the PR
- Squash commits if necessary to create a clean history

### Pull Request Description
- Brief summary of changes
- Issue numbers addressed (if any)
- Any special instructions for reviewers
- Screenshots or recordings if UI changes are involved

### Review Process
- Assign at least one technical reviewer; chapter/content changes also require one content reviewer
- Address all review feedback within 2 business days or post a blocker update
- Make requested changes
- Wait for approval before merging
- Ensure continuous integration checks pass

## 5. Code Review Guidelines

### For Reviewers
- Check that code follows style guidelines
- Verify functionality works as described
- Look for potential bugs or edge cases
- Ensure changed behavior is covered by at least one automated test (unit/integration/e2e)
- Consider performance implications
- Check for security vulnerabilities
- Verify accessibility requirements are met

### For Contributors
- Respond to review comments within 2 business days
- Make requested changes
- Explain your reasoning when disagreeing with requested changes
- Ask questions if feedback is unclear
- Thank reviewers for their time

## 6. Issue Management

### Creating Issues
- Use descriptive titles
- Provide detailed steps to reproduce (for bugs)
- Include expected vs. actual behavior
- Add at least one type label (bug/feature/docs) and one priority label
- Assign milestone if applicable

### Working on Issues
- Comment to indicate you're working on an issue
- Reference the issue in your commit messages
- Close the issue when your PR is merged

## 7. Documentation Standards

### Code Documentation
- Write clear, concise comments
- Document public APIs thoroughly
- Update documentation when making changes
- Use markdown consistently in docs comments (headings, fenced code blocks with language tag, and valid links)

### External Documentation
- Follow the Content Style Guide
- Use markdown hierarchy exactly as defined in this constitution (`#` -> `##` -> `###` without skips)
- Include examples where helpful
- Keep documentation up to date

## 8. Security Guidelines

### Reporting Security Issues
- Do not create public issues for security vulnerabilities
- Contact the security team directly
- Provide detailed information about the vulnerability
- Allow time for proper resolution before disclosure

### Secure Coding Practices
- Validate and sanitize all inputs
- Use parameterized queries to prevent SQL injection
- Implement proper authentication and authorization
- Protect against common web vulnerabilities
- Follow security best practices for dependencies

## 9. Community Guidelines

### Code of Conduct
- Be respectful and inclusive
- Provide constructive feedback
- Welcome new contributors
- Focus on technical merit
- Resolve conflicts constructively

### Communication
- Use appropriate channels for different topics
- Be patient with newcomers
- Provide helpful explanations
- Keep discussions productive

## 10. Project Maintenance

### Dependency Updates
- Regularly update dependencies
- Test after updates
- Monitor for security vulnerabilities
- Update lock files appropriately

### Code Maintenance
- Refactor legacy code when encountered
- Remove unused code
- Improve performance where possible
- Address technical debt

---

*This Contributor Handbook serves as the definitive reference for all contributors to the Physical AI & Humanoid Robotics Textbook project.*


### Source: docs/process/quality-assurance-checklist.md

# Quality Assurance Checklist

> **Note**: This is a companion document to the Project Constitution. For project 
> governance, scope, and objectives, see [constitution.md](../../constitution.md).
> 
> **Related Guides**: 
> - [Technical Implementation Guide](../architecture/technical-implementation-guide.md) - For implementation details
> - [Security Guidelines](../security/security-guidelines.md) - For security testing
> - [Content Style Guide](../process/content-style-guide.md) - For content quality

## 1. Content Quality Standards

### Technical Accuracy Verification
- [ ] All technical information verified against official documentation
- [ ] Code examples tested and functional
- [ ] Mathematical formulas accurate and properly formatted
- [ ] Hardware specifications reflect current market offerings
- [ ] All claims about technology capabilities substantiated
- [ ] Links to external resources are valid and current

### Clarity and Accessibility
- [ ] Written for students with AI fundamentals but new to robotics
- [ ] Technical terms defined on first use
- [ ] Progressive disclosure implemented (simple → complex)
- [ ] Complex concepts broken into digestible parts
- [ ] Active voice used wherever possible
- [ ] Jargon avoided when simpler alternatives exist
- [ ] Specific rather than vague language used

### Tone and Voice Consistency
- [ ] Professional but approachable tone maintained
- [ ] Encouraging and supportive language used
- [ ] Conversational without being informal
- [ ] Inclusive and welcoming to diverse audiences
- [ ] Confident but not condescending
- [ ] "You" used to address the reader directly
- [ ] Terminology consistent throughout

## 2. Chapter Structure Compliance

### Required Sections Present
- [ ] Chapter Title - Clear, descriptive title indicating main topic
- [ ] Learning Objectives - 3-5 specific, measurable outcomes
- [ ] Prerequisites - Knowledge/skills required before starting
- [ ] Introduction - Context and motivation for the chapter
- [ ] Core Concepts - Detailed explanations with examples
- [ ] Hands-On Practice - Step-by-step tutorials or exercises
- [ ] Assessment - Knowledge check questions and practical exercises
- [ ] Further Resources - Links to documentation, research, community
- [ ] Summary - Key takeaways and connection to next chapter

### Section-Specific Requirements
- [ ] Learning objectives use action verbs and are measurable
- [ ] Prerequisites are specific and include at least one review resource link when prerequisite knowledge is outside prior chapters
- [ ] Introduction establishes relevance to broader curriculum
- [ ] Core concepts include visual aids and consistent terminology
- [ ] Hands-on practice includes expected outputs and troubleshooting tips
- [ ] Assessment includes both knowledge checks and practical exercises
- [ ] Further resources include at least 2 links, with at least 1 official source updated within the last 24 months
- [ ] Summary connects to next chapter or concept

## 3. Code Quality Standards

### Language-Specific Conventions
- [ ] Python code follows PEP 8 style guide
- [ ] JavaScript/TypeScript uses consistent indentation (2 spaces)
- [ ] Shell/Bash follows consistent quoting and spacing
- [ ] Configuration files follow language-specific best practices

### Comment Requirements
- [ ] Comments explain the "why" not just the "what"
- [ ] Inline comments used sparingly but strategically
- [ ] Docstrings included for functions and classes
- [ ] Complex algorithms commented thoroughly
- [ ] Comments updated when code changes

### Example Quality Standards
- [ ] Code examples are complete and functional
- [ ] Error handling included for snippets that perform I/O, parsing, or network calls
- [ ] Meaningful variable and function names used
- [ ] Principle of least surprise followed
- [ ] Non-obvious parts explained with comments
- [ ] Examples tested in target environment
- [ ] Examples focused on concept being taught

## 4. Media Quality Standards

### Image Requirements
- [ ] New raster images use WebP (PNG/JPEG only for compatibility or transparency constraints)
- [ ] New images are <= 200KB, or PR includes documented exception + compressed variant
- [ ] Descriptive alt text provided for all images
- [ ] Minimum 72 DPI resolution for screen display
- [ ] Aspect ratio maintained, no distortion
- [ ] Descriptive, lowercase file names with hyphens

### Video Specifications
- [ ] Format is MP4 with H.264 codec
- [ ] Minimum 720p resolution, 1080p preferred
- [ ] 30fps standard frame rate
- [ ] Clear, noise-free audio with consistent volume
- [ ] Closed captions provided for accessibility
- [ ] Instructional videos are <= 5 minutes (demo/overview videos <= 10 minutes)
- [ ] Relevant thumbnail image provided

### Diagram Standards
- [ ] Consistent visual language throughout
- [ ] Color-blind friendly palettes used
- [ ] Diagram labels are readable at 100% zoom with minimum equivalent size of 14px
- [ ] Arrows/connectors used consistently to show relationships
- [ ] Legends included whenever a diagram uses 3 or more colors, symbols, or line styles
- [ ] High-resolution PNG or SVG format exported

## 5. Accessibility Compliance

### Alt Text Verification
- [ ] Meaningful alt text provided for all images
- [ ] Content and function of images described
- [ ] Alt text concise but informative
- [ ] Empty alt text (`alt=""`) used for decorative images
- [ ] Extended descriptions provided for complex diagrams

### Color Usage Verification
- [ ] Sufficient contrast ratios maintained (minimum 4.5:1 for normal text)
- [ ] Color not relied upon solely to convey information
- [ ] Color-blind friendly palettes used
- [ ] Color combinations tested with accessibility tools
- [ ] Text alternatives provided for color-coded information

### Font and Sizing Verification
- [ ] Web-safe fonts or properly licensed web fonts used, with fallback font declared in CSS stack
- [ ] Readable font sizes maintained (minimum 16px for body text)
- [ ] Relative units (em, rem) used for scalability
- [ ] Text can be resized up to 200% without loss of functionality
- [ ] Proper line height maintained for readability (1.4-1.6)

## 6. Markdown Formatting Compliance

### Header Hierarchy Verification
- [ ] `#` used for main chapter titles
- [ ] `##` used for major sections
- [ ] `###` used for subsections
- [ ] `####` used for sub-subsections (sparingly)
- [ ] Header levels not skipped (no jump from `##` to `####`)

### List Formatting Verification
- [ ] `-` used for unordered lists
- [ ] `1.`, `2.`, `3.` used for ordered lists
- [ ] Consistent indentation maintained (2 spaces)
- [ ] Exactly one blank line before and after top-level lists (except when list follows a heading directly)
- [ ] Nested lists indented with 2 spaces per level

### Link Convention Verification
- [ ] Descriptive link text used rather than URLs
- [ ] Links placed immediately after relevant text
- [ ] Relative links used for internal references
- [ ] Absolute URLs used for external references
- [ ] All links verified as functional

## 7. Security Testing

### Input Validation Testing
- [ ] All user inputs validated and sanitized
- [ ] Potential injection attacks prevented (SQL, XSS, etc.)
- [ ] If file uploads exist, MIME type, extension, and size limits are validated server-side
- [ ] Rate limiting implemented and tested
- [ ] Protected endpoints return 401/403 in automated tests for unauthorized access

### Data Protection Verification
- [ ] Sensitive data encrypted at rest
- [ ] Data encrypted in transit using TLS
- [ ] PII fields are classified, minimized, and masked/redacted in logs
- [ ] Session management secure
- [ ] No hardcoded secrets in repository and secret scanning passes in CI

### Data Retention & Deletion Verification
- [ ] Chat message retention TTL configured (default: 30 days) and enforced by scheduled cleanup
- [ ] Session retention TTL configured (default: 24 hours inactivity) and enforced
- [ ] Backup retention period configured (default: 30 days) with automatic pruning enabled
- [ ] User data deletion request process documented and validated end-to-end within 7 days
- [ ] Audit logs capture actor, action, timestamp, resource, and outcome for auth/content mutation events

## 8. Performance Testing

### Response Time Verification
- [ ] Non-LLM API endpoints (auth/profile/content metadata) meet p95 <= 1 second
- [ ] Page load times under 2 seconds
- [ ] LLM endpoints meet their declared p95 targets in this constitution (`/chat <= 3s`, `/personalize <= 4s`, `/translate <= 5s`, `/agents/* <= 4.5s`)
- [ ] Database queries optimized
- [ ] Caching policy documented for hot read paths, with at least one cache hit-rate metric tracked in monitoring

### Scalability Testing
- [ ] System handles expected concurrent users
- [ ] Resource usage monitored under load
- [ ] Failover mechanisms tested
- [ ] Backup and recovery procedures verified
- [ ] Monitoring includes uptime, error-rate, and latency metrics with at least one configured alert per metric

## 9. Cross-Browser Compatibility

### Browser Testing
- [ ] Functionality verified on Chrome
- [ ] Functionality verified on Firefox
- [ ] Functionality verified on Safari
- [ ] Functionality verified on Edge
- [ ] Responsive design verified on mobile devices

## 10. Final Verification Checklist

### Pre-Release Verification
- [ ] All content quality standards met
- [ ] All accessibility requirements satisfied
- [ ] All security measures implemented and tested
- [ ] Performance benchmarks met
- [ ] Cross-browser compatibility verified
- [ ] All links and references functional
- [ ] All media assets pass format/size/accessibility checks defined in Sections 4 and 5
- [ ] Code examples tested and functional
- [ ] Documentation complete and accurate
- [ ] User experience tested and validated

---

*This Quality Assurance Checklist serves as the definitive reference for verifying the quality of all components in the Physical AI & Humanoid Robotics Textbook project.*


### Source: docs/security/security-guidelines.md

# Security & Compliance Guide

> **Note**: This is a companion document to the Project Constitution. For project 
> governance, scope, and objectives, see [constitution.md](../../constitution.md).
> 
> **Related Guides**: 
> - [Technical Implementation Guide](../architecture/technical-implementation-guide.md) - For implementation details
> - [Deployment Guide](../deployment/deployment-guide.md) - For infrastructure security
> - [Quality Assurance Checklist](../process/quality-assurance-checklist.md) - For security testing

## 1. Security Architecture Overview

The Physical AI & Humanoid Robotics Textbook platform implements a defense-in-depth security architecture with multiple layers of protection:

- **Network Layer**: Firewall rules, DDoS protection, secure network segmentation
- **Application Layer**: Input validation, authentication, authorization, secure coding practices
- **Data Layer**: Encryption at rest and in transit, access controls, audit logging
- **Infrastructure Layer**: Container security, host security, patch management

## 2. Authentication & Authorization

### Better-Auth Implementation
```python
from better_aur import BetterAuth, Session
from fastapi import Depends, HTTPException, status
import os

# Initialize Better-Auth
auth = BetterAuth(
    secret=os.getenv("AUTH_SECRET"),
    cookie_name="session_token",
    expiration_time=86400  # 24 hours
)

# Google OAuth configuration
auth.register_oauth_provider(
    "google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    redirect_uri="http://localhost:3000/api/auth/callback/google"
)

# GitHub OAuth configuration
auth.register_oauth_provider(
    "github",
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    redirect_uri="http://localhost:3000/api/auth/callback/github"
)
```

### JWT Token Handling
```python
import jwt
from datetime import datetime, timedelta
from typing import Optional

class JWTHandler:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def encode_token(self, user_id: str, expires_delta: Optional[timedelta] = None) -> str:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=24)
        
        to_encode = {"user_id": user_id, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
```

### Session Management
```python
from typing import Optional
import redis
import os
import uuid

class SessionManager:
    def __init__(self):
        self.redis_client = redis.from_url(os.getenv("REDIS_URL"))
        self.session_ttl = 86400  # 24 hours

    def create_session(self, user_id: str) -> str:
        session_id = str(uuid.uuid4())
        session_data = {"user_id": user_id, "created_at": datetime.utcnow().isoformat()}
        
        self.redis_client.setex(
            f"session:{session_id}", 
            self.session_ttl, 
            json.dumps(session_data)
        )
        
        return session_id

    def get_session(self, session_id: str) -> Optional[dict]:
        session_data = self.redis_client.get(f"session:{session_id}")
        if session_data:
            return json.loads(session_data)
        return None

    def delete_session(self, session_id: str):
        self.redis_client.delete(f"session:{session_id}")

    def extend_session(self, session_id: str):
        self.redis_client.expire(f"session:{session_id}", self.session_ttl)
```

## 3. API Security

### CORS Configuration
```python
from fastapi.middleware.cors import CORSMiddleware
import os

# Get allowed origins from environment
allowed_origins = os.getenv("CORS_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count", "X-Request-ID"],
    max_age=600,  # Cache preflight requests for 10 minutes
)
```

### Rate Limiting Implementation
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Apply rate limits to endpoints
@app.post("/api/v1/chat/query")
@limiter.limit("60/minute")  # 60 requests per minute per IP
async def chat_query(request: Request, query: ChatQuery):
    # Implementation here
    pass

@app.post("/api/v1/auth/login")
@limiter.limit("5/minute")  # Lower limit for auth endpoints
async def login(request: Request, credentials: Credentials):
    # Implementation here
    pass
```

### Input Validation
```python
from pydantic import BaseModel, validator, Field
from typing import Optional
import re

class ChatQuery(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    chapter_context: Optional[str] = Field(None, max_length=50)
    selected_text: Optional[str] = Field(None, max_length=5000)

    @validator('query')
    def validate_query(cls, v):
        # Sanitize input
        if len(v.strip()) == 0:
            raise ValueError("Query cannot be empty")

        # Check for potential injection attempts
        dangerous_patterns = [
            r'<script[^>]*>.*?</script>',  # XSS attempts
            r'javascript:',  # JavaScript URLs
            r'on\w+\s*=',  # Event handlers
            r'eval\s*\(',  # eval function
            r'exec\s*\(',  # exec function
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError("Invalid query content detected")

        return v.strip()

    @validator('chapter_context')
    def validate_chapter_context(cls, v):
        if v is not None:
            # Only allow alphanumeric, hyphens, and underscores
            if not re.match(r'^[a-zA-Z0-9_-]+$', v):
                raise ValueError("Invalid chapter context format")
        return v
```

### SQL Injection Prevention
```python
from sqlalchemy import text
from typing import List, Dict, Optional

class UserService:
    def __init__(self, db_session):
        self.db = db_session

    async def get_user_by_email(self, email: str) -> Optional[Dict]:
        """
        Safely retrieve user by email using parameterized queries
        """
        query = text("SELECT user_id, email, created_at FROM users WHERE email = :email")
        result = await self.db.execute(query, {"email": email})
        row = result.fetchone()
        
        if row:
            return {
                "user_id": row.user_id,
                "email": row.email,
                "created_at": row.created_at
            }
        return None

    async def get_user_progress(self, user_id: str, chapter_ids: List[str]) -> List[Dict]:
        """
        Safely retrieve user progress for specific chapters
        """
        # Validate input
        if not all(isinstance(cid, str) and len(cid) <= 50 for cid in chapter_ids):
            raise ValueError("Invalid chapter IDs")
        
        # Use parameterized query with IN clause
        placeholders = ','.join([f':cid{i}' for i in range(len(chapter_ids))])
        query = text(f"""
            SELECT chapter_id, completion_percentage, time_spent_seconds 
            FROM chapter_progress 
            WHERE user_id = :user_id AND chapter_id IN ({placeholders})
        """)
        
        params = {"user_id": user_id}
        params.update({f"cid{i}": chapter_ids[i] for i in range(len(chapter_ids))})
        
        result = await self.db.execute(query, params)
        rows = result.fetchall()
        
        return [
            {
                "chapter_id": row.chapter_id,
                "completion_percentage": row.completion_percentage,
                "time_spent_seconds": row.time_spent_seconds
            }
            for row in rows
        ]
```

## 4. Data Protection

### Encryption at Rest
```python
from cryptography.fernet import Fernet
import base64
import os

class DataEncryption:
    def __init__(self, key: bytes):
        self.fernet = Fernet(key)

    def encrypt(self, data: str) -> str:
        """Encrypt sensitive data"""
        encrypted = self.fernet.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        decoded = base64.b64decode(encrypted_data.encode())
        decrypted = self.fernet.decrypt(decoded)
        return decrypted.decode()

# Usage
encryption_key = os.getenv("ENCRYPTION_KEY").encode()
crypto = DataEncryption(encryption_key)

# Encrypt PII before storing
user.email_encrypted = crypto.encrypt(user.email)
```

### Encryption in Transit
```python
# Ensure HTTPS is enforced
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

# Add to app if in production
if os.getenv("APP_ENV") == "production":
    app.add_middleware(HTTPSRedirectMiddleware)

# Database connection with SSL
DATABASE_URL = os.getenv("DATABASE_URL")
if os.getenv("APP_ENV") == "production":
    DATABASE_URL += "?sslmode=require"
```

### PII Handling Code Examples
```python
import hashlib
from typing import Dict, Any

class PIIHandler:
    @staticmethod
    def anonymize_email(email: str) -> str:
        """Anonymize email for logging purposes"""
        if "@" in email:
            local, domain = email.split("@", 1)
            if len(local) > 2:
                masked_local = local[0] + "*" * (len(local) - 2) + local[-1]
            else:
                masked_local = "*" * len(local)
            return f"{masked_local}@{domain}"
        return "***"

    @staticmethod
    def hash_identifier(identifier: str) -> str:
        """Hash identifiers for analytics while preserving uniqueness"""
        return hashlib.sha256(identifier.encode()).hexdigest()

    @staticmethod
    def sanitize_log_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Remove or mask PII from log data"""
        sanitized = data.copy()
        
        # Remove sensitive fields
        sensitive_fields = ["password", "token", "api_key", "secret"]
        for field in sensitive_fields:
            if field in sanitized:
                sanitized[field] = "***REDACTED***"
        
        # Mask email addresses
        if "email" in sanitized:
            sanitized["email"] = PIIHandler.anonymize_email(sanitized["email"])
        
        # Hash user IDs for analytics
        if "user_id" in sanitized:
            sanitized["user_id"] = PIIHandler.hash_identifier(sanitized["user_id"])
        
        return sanitized
```

## 5. Privacy Compliance

### GDPR Considerations
- **Right to Access**: Users can request a copy of their data
- **Right to Rectification**: Users can update their personal information
- **Right to Erasure**: Users can request deletion of their account and data
- **Right to Data Portability**: Users can export their data in a structured format
- **Consent Management**: Clear consent mechanisms for data processing

### CCPA Considerations
- **Right to Know**: Users can request information about collected data
- **Right to Delete**: Users can request deletion of their personal information
- **Right to Opt-Out**: Users can opt-out of sale of personal information
- **Non-Discrimination**: No penalty for exercising privacy rights

### Data Retention Policies
```python
from datetime import datetime, timedelta
from typing import List

class DataRetentionManager:
    def __init__(self, db_session):
        self.db = db_session

    async def cleanup_expired_data(self):
        """Remove data that exceeds retention periods"""
        # Delete chat messages older than 1 year
        one_year_ago = datetime.utcnow() - timedelta(days=365)
        await self.db.execute(
            text("DELETE FROM chat_messages WHERE created_at < :cutoff"),
            {"cutoff": one_year_ago}
        )

        # Delete inactive user accounts older than 3 years
        three_years_ago = datetime.utcnow() - timedelta(days=1095)
        await self.db.execute(
            text("""
                DELETE FROM users 
                WHERE last_login < :cutoff 
                AND is_active = false
            """),
            {"cutoff": three_years_ago}
        )

        # Archive old analytics data
        six_months_ago = datetime.utcnow() - timedelta(days=180)
        await self.archive_old_analytics(six_months_ago)

    async def archive_old_analytics(self, cutoff_date: datetime):
        """Move old analytics data to archive table"""
        await self.db.execute(
            text("""
                INSERT INTO analytics_archive 
                SELECT * FROM analytics 
                WHERE timestamp < :cutoff
            """),
            {"cutoff": cutoff_date}
        )
        
        # Remove from main table
        await self.db.execute(
            text("DELETE FROM analytics WHERE timestamp < :cutoff"),
            {"cutoff": cutoff_date}
        )
```

## 6. Security Best Practices

### Secret Management
```python
import os
from typing import Optional

class SecretManager:
    @staticmethod
    def get_secret(secret_name: str, default: Optional[str] = None) -> str:
        """Securely retrieve secrets from environment variables"""
        secret = os.getenv(secret_name)
        if not secret and default is None:
            raise ValueError(f"Required secret {secret_name} not found")
        return secret or default

    @staticmethod
    def validate_secrets():
        """Validate that all required secrets are present"""
        required_secrets = [
            "DATABASE_URL",
            "COHERE_API_KEY",
            "QDRANT_API_KEY",
            "ENCRYPTION_KEY",
            "AUTH_SECRET"
        ]
        
        missing_secrets = []
        for secret in required_secrets:
            if not os.getenv(secret):
                missing_secrets.append(secret)
        
        if missing_secrets:
            raise ValueError(f"Missing required secrets: {', '.join(missing_secrets)}")
```

### Dependency Scanning
```bash
# Scan for vulnerabilities in dependencies
pip install safety
safety check -r requirements.txt

# Use pip-audit for more detailed analysis
pip install pip-audit
pip-audit -r requirements.txt
```

### Security Headers
```python
from starlette.middleware.security import SecurityMiddleware

# Add security headers
app.add_middleware(
    SecurityMiddleware,
    content_security_policy="default-src 'self'; script-src 'self' 'unsafe-inline' https://www.google-analytics.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' https:; connect-src 'self' https://*.qdrant.io https://api.cohere.ai;",
    strict_transport_security_max_age=31536000,
    strict_transport_security_include_subdomains=True,
    strict_transport_security_preload=True,
    referrer_policy="strict-origin-when-cross-origin",
)
```

## 7. Incident Response

### Security Incident Procedures
```python
import logging
from datetime import datetime
from typing import Dict, Any

class SecurityIncidentHandler:
    def __init__(self):
        self.logger = logging.getLogger("security")
    
    def report_incident(self, incident_type: str, details: Dict[str, Any]):
        """Log and report security incidents"""
        incident_report = {
            "timestamp": datetime.utcnow().isoformat(),
            "incident_type": incident_type,
            "details": details,
            "severity": self._determine_severity(incident_type)
        }
        
        # Log incident
        self.logger.error(f"SECURITY INCIDENT: {incident_report}")
        
        # Trigger alerts based on severity
        if incident_report["severity"] in ["HIGH", "CRITICAL"]:
            self._trigger_alert(incident_report)
    
    def _determine_severity(self, incident_type: str) -> str:
        """Determine incident severity based on type"""
        critical_types = [
            "data_breach", "unauthorized_access", "sql_injection", 
            "xss_attack", "csrf_attack", "ddos_attack"
        ]
        
        high_types = [
            "failed_login", "suspicious_activity", "brute_force_attempt",
            "malformed_request", "rate_limit_violation"
        ]
        
        if incident_type in critical_types:
            return "CRITICAL"
        elif incident_type in high_types:
            return "HIGH"
        else:
            return "MEDIUM"
    
    def _trigger_alert(self, incident_report: Dict[str, Any]):
        """Trigger alert notifications"""
        # Send to security team
## Moved Code Snippets Archive

This file contains content moved from `constitution.md` lines 2800-5200.

### Appendix B: Minimal CI/CD (Hackathon)

- Pull request: lint + unit smoke checks.
- Main branch: build + manual deploy to demo environment.
- Pre-demo: health check + one golden query test.

### Appendix C: Security Baseline

- Rate limiting on all mutation endpoints.
- Strict request schema validation.
- No secrets in repository.
- TLS for all external traffic.
