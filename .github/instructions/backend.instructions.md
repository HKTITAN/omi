---
applyTo: "backend/**/*.py"
excludeAgent: "code-review"
---

## Backend (Python/FastAPI) instructions

- **No in-function imports**. All imports must be at module top-level.
- **Follow the strict layer hierarchy** (lowest → highest):
  - `backend/database/` → `backend/utils/` → `backend/routers/` → `backend/main.py`
  - Never import from higher layers in lower layers (e.g., `utils` must not import from `routers`).
- **Memory-first**: changes to conversation processing, storage, or extraction must not risk missing/corrupting memories.
- Free large objects promptly (`del`, `.clear()`) when handling audio bytes, transcripts, large dicts/lists.

### Where to look first

- Conversation processing pipeline: `backend/utils/conversations/process_conversation.py`
- Chat routing/LangGraph: `backend/utils/retrieval/graph.py`
- WebSocket transcription: `backend/routers/transcribe.py`

### How to verify

If you changed backend code, run:

```bash
cd backend
./test.sh
```

