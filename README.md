# Physical AI & Humanoid Robotics Textbook

An AI-native textbook for Physical AI and Humanoid Robotics, built for Panaversity Hackathon I. Features a Docusaurus-based textbook with an integrated RAG chatbot, selected-text Q&A, content personalization, Urdu translation, and LLM-powered subagents.

## Quick Start (Ubuntu 22.04)

### Prerequisites

- Docker and Docker Compose
- Git
- A Neon Postgres free-tier account
- A Qdrant Cloud free-tier account
- An OpenRouter API key

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/metachemist/physical-ai-textbook-with-rag-01.git
cd physical-ai-textbook-with-rag-01

# 2. Configure environment variables
cp backend/.env.example backend/.env
# Edit backend/.env with your actual credentials:
#   DATABASE_URL     — Neon Postgres connection string
#   QDRANT_URL       — Qdrant Cloud cluster URL
#   QDRANT_API_KEY   — Qdrant Cloud API key
#   OPENROUTER_API_KEY — OpenRouter API key

# 3. Start both services
docker compose up
```

### Verify

- **Frontend**: http://localhost:3000 — Docusaurus textbook site
- **Backend**: http://localhost:8000/health — API health check (should return `{"status": "healthy"}`)

## Architecture

```
┌─────────────────┐     ┌─────────────────────┐
│   Docusaurus     │────▶│   FastAPI Backend    │
│   (GitHub Pages) │     │   (Render Free Tier) │
│                  │     │                      │
│  - 13 chapters   │     │  - /health           │
│  - ChatPanel     │     │  - /api/v1/chat      │
│  - AuthModal     │     │  - /api/v1/ingest    │
│  - Personalize   │     │  - /api/v1/personalize│
│  - Translate     │     │  - /api/v1/translate  │
└─────────────────┘     │  - /api/v1/agents/*  │
                        └───────┬───────┬──────┘
                                │       │
                   ┌────────────┘       └────────────┐
                   ▼                                  ▼
          ┌────────────────┐               ┌─────────────────┐
          │ Qdrant Cloud   │               │ Neon Postgres    │
          │ (Vector Store) │               │ (Relational DB)  │
          │                │               │                  │
          │ physical_ai_   │               │ users, sessions, │
          │ textbook (384d)│               │ messages,        │
          └────────────────┘               │ user_profiles    │
                                           └─────────────────┘
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Docusaurus 3.x (TypeScript) |
| Backend | FastAPI 0.111+ (Python 3.11) |
| Agent Framework | OpenAI Agents SDK |
| Vector Store | Qdrant Cloud Free Tier |
| Relational DB | Neon Serverless Postgres |
| LLM Gateway | OpenRouter (configurable model) |
| Embedding | sentence-transformers/all-MiniLM-L6-v2 (local) |
| Auth | Better-Auth (Node.js microservice) |
| Deployment | GitHub Pages (frontend), Render (backend) |

## Project Structure

```
├── frontend/           # Docusaurus textbook site
│   ├── docs/           # 13 chapter MDX files (4 modules)
│   ├── src/components/ # ChatPanel, AuthModal
│   └── docusaurus.config.ts
├── backend/            # FastAPI backend
│   ├── app/
│   │   ├── main.py     # App factory + lifespan
│   │   ├── config.py   # Pydantic Settings
│   │   ├── api/        # Route handlers
│   │   ├── services/   # Business logic (RAG, chunker, embedder)
│   │   └── db/         # Database access
│   ├── alembic/        # Schema migrations
│   └── tests/          # Unit, integration, golden eval
├── auth/               # Better-Auth microservice (Phase 3)
├── specs/              # Specification artifacts
│   ├── 1-specify/spec.md
│   ├── 2-plan/plan.md
│   └── 3-tasks/tasks.md
├── docker-compose.yaml
└── constitution.md     # Project governance
```

## CI/CD

- **CI** (`.github/workflows/ci.yml`): Runs on every PR — builds frontend, lints backend with ruff
- **Pages** (`.github/workflows/pages.yml`): Deploys to GitHub Pages on merge to main

## Links

- [Project Constitution](./constitution.md)
- [Quick Start Guide](./Quick-Start-Guide.md)
- [Feature Spec](./specs/1-specify/spec.md)
- [Implementation Plan](./specs/2-plan/plan.md)
- [Task List](./specs/3-tasks/tasks.md)
