# Data Model: Physical AI Textbook (All Phases)

**Branch**: `specification` | **Date**: 2026-03-13 | **Plan**: [plan.md](plan.md)

---

## Relational Database (Neon Serverless Postgres)

### Table: `users`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `uuid` | PK, default gen_random_uuid() | Better-Auth user ID |
| `name` | `text` | NOT NULL | Display name |
| `email` | `text` | UNIQUE, NOT NULL | Login credential |
| `email_verified` | `boolean` | NOT NULL, default false | Better-Auth field |
| `image` | `text` | nullable | Profile image URL |
| `created_at` | `timestamptz` | NOT NULL, default now() | |
| `updated_at` | `timestamptz` | NOT NULL, default now() | |

### Table: `accounts` (Better-Auth)

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `uuid` | PK | |
| `user_id` | `uuid` | FK → users.id, NOT NULL | |
| `account_id` | `text` | NOT NULL | Provider-specific ID |
| `provider_id` | `text` | NOT NULL | e.g. `"credential"` |
| `password` | `text` | nullable | bcrypt hash for credential provider |
| `access_token` | `text` | nullable | |
| `refresh_token` | `text` | nullable | |
| `expires_at` | `timestamptz` | nullable | |
| `created_at` | `timestamptz` | NOT NULL, default now() | |
| `updated_at` | `timestamptz` | NOT NULL, default now() | |

### Table: `sessions`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `uuid` | PK | |
| `user_id` | `uuid` | FK → users.id, NOT NULL | |
| `token` | `text` | UNIQUE, NOT NULL | Session token (JWT or opaque) |
| `expires_at` | `timestamptz` | NOT NULL | TTL = 24h from creation |
| `ip_address` | `text` | nullable | |
| `user_agent` | `text` | nullable | |
| `created_at` | `timestamptz` | NOT NULL, default now() | |
| `updated_at` | `timestamptz` | NOT NULL, default now() | |

### Table: `verification` (Better-Auth)

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `uuid` | PK | |
| `identifier` | `text` | NOT NULL | email or token identifier |
| `value` | `text` | NOT NULL | verification token |
| `expires_at` | `timestamptz` | NOT NULL | |
| `created_at` | `timestamptz` | NOT NULL, default now() | |
| `updated_at` | `timestamptz` | NOT NULL, default now() | |

### Table: `user_profiles`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `user_id` | `uuid` | PK, FK → users.id | One profile per user |
| `python_level` | `text` | NOT NULL | `beginner` / `intermediate` / `advanced` |
| `ros_experience` | `boolean` | NOT NULL | Yes/No robotics experience |
| `ai_knowledge` | `text` | NOT NULL | `beginner` / `intermediate` / `advanced` |
| `created_at` | `timestamptz` | NOT NULL, default now() | |
| `updated_at` | `timestamptz` | NOT NULL, default now() | |

**Derived track** (computed at read time, never stored):

```
IF ros_experience = true                                   → hardware/robotics
ELSE IF python_level = advanced AND ai_knowledge IN (intermediate, advanced) → accelerated
ELSE IF python_level IN (intermediate, advanced)           → software_engineer
ELSE                                                       → beginner
```

### Table: `messages`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `uuid` | PK | |
| `session_id` | `text` | NOT NULL, indexed | Browser session ID (not auth session) |
| `user_id` | `uuid` | nullable | null = anonymous |
| `chapter_id` | `text` | NOT NULL | Chapter context |
| `role` | `text` | NOT NULL | `user` / `assistant` |
| `content` | `text` | NOT NULL | Message text |
| `citations` | `jsonb` | nullable | Array of citation objects |
| `selected_text` | `text` | nullable | User's highlighted text (user messages only) |
| `created_at` | `timestamptz` | NOT NULL, default now() | |

**Session window**: Rolling last 3–5 exchanges fetched by `session_id` ordered by `created_at DESC LIMIT 10`.

---

## Vector Store (Qdrant Cloud)

### Collection: `physical_ai_textbook`

**Config**:
- Distance: `Cosine`
- Vector size: `384` (sentence-transformers/all-MiniLM-L6-v2)
- On-disk payload indexing: enabled for `chapter_id`, `section_id`

### Point Schema

| Field | Type | Notes |
|-------|------|-------|
| `id` | UUID (string) | Deterministic: `uuid5(NAMESPACE_URL, f"physical-ai-textbook:{chapter_id}:{chunk_index}")` |
| vector | `float32[384]` | all-MiniLM-L6-v2 embedding |

**Payload**:

| Key | Type | Notes |
|-----|------|-------|
| `chapter_id` | string | e.g. `week-01-ros2-fundamentals` |
| `module_id` | string | e.g. `module-1-ros2` |
| `section_id` | string | e.g. `ros2-nodes-and-topics` (slug) |
| `section_heading` | string | `"ROS 2 Nodes and Topics"` (human-readable, for citation display) |
| `source_url` | string | `/docs/module-1-ros2/week-01-ros2-fundamentals#ros2-nodes-and-topics` |
| `chunk_index` | int | Position within chapter (0-based); part of composite key |
| `token_count` | int | Actual token count of this chunk |
| `heading_level` | int | `2` for H2, `3` for H3 (supports citation quality ranking) |
| `text` | string | Raw chunk text (stored for zero-I/O citation display) |

**Composite identity key**: `(chapter_id, chunk_index)` — deterministic ID ensures idempotent upsert.

---

## In-Memory / Session State (Browser)

### Chat Session (React state, not persisted)

```typescript
interface ChatSession {
  sessionId: string;           // uuid generated on page load
  chapterId: string;           // current chapter
  exchanges: Exchange[];       // rolling window, max 5
  selectedText: string | null; // current text selection
  status: 'idle' | 'submitting' | 'streaming' | 'complete' | 'error';
  lastError: string | null;
}

interface Exchange {
  id: string;
  question: string;
  selectedText: string | null;
  answer: string;
  citations: Citation[];
  latencyMs: number;
}

interface Citation {
  chapterId: string;
  sectionId: string;
  sourceUrl: string;
}
```

---

## Domain Entities (Logical, Cross-Cutting)

### Module

| Attribute | Type | Notes |
|-----------|------|-------|
| `moduleId` | string | e.g. `module-1` |
| `title` | string | e.g. `ROS 2 Fundamentals` |
| `chapters` | Chapter[] | Ordered list |
| `weekRange` | string | e.g. `Weeks 1–5` |

4 modules total: ROS 2 Fundamentals (Weeks 1–5), Simulation/Gazebo/Unity (Weeks 6–7), NVIDIA Isaac (Weeks 8–10), VLA/Humanoid (Weeks 11–13).

### Chapter

| Attribute | Type | Notes |
|-----------|------|-------|
| `chapterId` | string | e.g. `module-1-ros2-week1` |
| `moduleId` | string | FK → Module |
| `weekNumber` | int | 1–13 |
| `wordCount` | int | Min 800 prose words |
| `reviewStatus` | enum | `draft` / `ai_assisted` / `peer_reviewed` / `expert_reviewed` / `published` |
| `docPath` | string | Relative path in Docusaurus docs dir |

### Section

| Attribute | Type | Notes |
|-----------|------|-------|
| `sectionId` | string | Slug of heading text |
| `chapterId` | string | FK → Chapter |
| `headingText` | string | Raw heading text |
| `headingLevel` | int | 2 or 3 (H2/H3) |
| `sourceUrl` | string | `/docs/.../chapter-slug#section-slug` |

### Chunk (vector store unit)

Defined above in Qdrant schema. Composite key: `(chapterId, chunkIndex)`.

### Agent Invocation

| Attribute | Type | Notes |
|-----------|------|-------|
| `agentName` | enum | `quiz_generator` / `chapter_summarizer` / `prerequisite_mapper` |
| `chapterId` | string | Input chapter |
| `inputParams` | jsonb | difficulty, level, topic, count |
| `groundingChunks` | string[] | Chunk IDs retrieved |
| `output` | jsonb | Agent-specific output |
| `latencyMs` | int | |
| `userId` | uuid | FK → users.id |

---

## State Transitions

### Chapter Review Status

```
draft → ai_assisted → peer_reviewed → expert_reviewed → published
```
A chapter MUST NOT be published until `expert_reviewed`.

### Chat Panel UI State

```
idle → submitting → streaming → complete
         ↓                        ↓
       error ←─────────────────────
       (retry → submitting)
```
