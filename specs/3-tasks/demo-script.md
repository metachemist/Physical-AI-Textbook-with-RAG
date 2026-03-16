# Demo Script — Physical AI & Humanoid Robotics Textbook

**Target runtime**: ≤90 seconds
**Segments**: 5
**Browser tabs**: 2 (app tab + GitHub tab)

---

## Segment 1 · Homepage & Navigation (0–15s)

1. Open the live app: `https://metachemist.github.io/physical-ai-textbook-with-rag-01/`
2. Say: *"This is the Physical AI Textbook — a 13-chapter AI-native learning platform."*
3. Click the **Module 1: ROS 2** sidebar category to expand it.
4. Click **Week 1: ROS 2 Fundamentals** to open the chapter.
5. Briefly scroll to show the learning objectives and a code block.

## Segment 2 · Chatbot with Selected Text (15–35s)

1. Highlight a sentence (≥20 chars) from the ROS 2 publisher section.
2. The **SelectedTextBadge** appears in the ChatPanel below.
3. Type: *"Can you explain this in simple terms?"* — press Enter.
4. The response streams in; the first paragraph directly addresses the highlighted passage.
5. Point to the citation link(s) at the bottom of the response.

## Segment 3 · Quiz Generator Agent (35–55s)

1. Click the **Quiz** button (auth-guard — sign in first if prompted).
2. Request: *"Give me 3 medium difficulty questions about this chapter."*
3. Show the returned JSON: 3 MCQs each with 4 options, `correctAnswer`, and `explanation`.

## Segment 4 · Personalization (55–70s)

1. Click the **Personalize** button in the SectionToolbar.
2. The prose rewrites inline for the user's derived track (shown in the response badge).
3. Click **Revert** to restore the original — no page reload.

## Segment 5 · Architecture & Submission Evidence (70–90s)

1. Switch to the GitHub tab: `https://github.com/metachemist/physical-ai-textbook-with-rag-01`
2. Point out: `backend/`, `frontend/`, `auth/`, `docker-compose.yaml`.
3. End with: *"Single `docker compose up`, GitHub Pages deploy, Render backend — all live."*

---

## Fallback Artifacts (keep on desktop)

| Artifact | Path |
|----------|------|
| (a) Chat response screenshot | `fallback/chat-response.png` |
| (b) Pre-authenticated backup tab | (open before recording) |
| (c) Urdu section screenshot | `fallback/urdu-section.png` |
| (d) Static fallback page | `fallback/index.html` |
