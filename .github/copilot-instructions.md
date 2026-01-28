# Omi repo instructions for GitHub Copilot Coding Agent

These instructions are **repository-wide**. They are designed to help Copilot Coding Agent make correct changes with minimal exploration and fewer rejected PRs.

## What this repository is

Omi is an open-source AI wearable system. It includes:

- `backend/` (Python, FastAPI): REST + WebSocket API, conversation processing, memory extraction, LangGraph-based chat, integrations.
- `app/` (Flutter/Dart): mobile/desktop app, BLE device comms, real-time audio streaming to backend.
- `omi/` and `omiGlass/` (C/C++ / Zephyr / Arduino): firmware for devices.
- `web/` (Next.js/TypeScript): web frontends (main + personas).
- `plugins/`: integration apps/plugins (Python + Node).
- `sdks/`: client SDKs (Python/Swift/React Native).
- `mcp/`: MCP server.

## Core product principle (do not break)

Omi is **memory-first**. Protect the core loop:

Capture → Understand → Remember → Retrieve → Act

If a change risks missing/corrupting memories, treat it as critical and be conservative.

## Backend architecture constraints (strict)

### Module hierarchy (imports)

Backend has a strict import/layer order (lowest → highest):

`backend/database/` → `backend/utils/` → `backend/routers/` → `backend/main.py`

Rules:
- **Never** import from higher layers in lower layers (e.g. `utils` must not import from `routers`).
- **No in-function imports** in Python (imports must be at module top-level).
- Free large objects promptly where relevant (`del`, `.clear()`).

### Key entry points (start here when investigating)

- Conversation processing: `backend/utils/conversations/process_conversation.py`
- Chat routing / LangGraph: `backend/utils/retrieval/graph.py`
- WebSocket audio streaming (`/v4/listen`): `backend/routers/transcribe.py`
- App conversation finalize: `backend/routers/conversations.py` (`POST /v1/conversations`)

Architecture references you can trust:
- `.cursor/ARCHITECTURE.md`
- `.cursor/DATA_FLOW.md`
- `.cursor/API_REFERENCE.md`
- `docs/doc/developer/backend/backend_deepdive.mdx`
- `docs/doc/developer/backend/chat_system.mdx`
- `docs/doc/developer/backend/StoringConversations.mdx`

## Validation: always run the right checks

Pick checks based on what you changed. Prefer these repo scripts/workflows (don’t invent new commands).

### Backend (Python/FastAPI)

Run unit tests:

```bash
cd backend
./test.sh
```

Notes:
- `backend/test.sh` sets `ENCRYPTION_SECRET` inside the script.

### App (Flutter)

Run tests:

```bash
cd app
./test.sh
```

Notes:
- `app/test.sh` bootstraps missing generated files and runs `flutter pub get` / `build_runner` if needed.

### Web (Next.js)

CI lint commands are defined in `.github/workflows/lint.yml`:

```bash
cd web/frontend
npm ci
npm run lint
npm run lint:format -- --check
```

```bash
cd web/personas-open-source
npm ci --legacy-peer-deps
npm run lint
```

## Behavior guidelines for the agent

- Prefer existing patterns; search for similar code before adding new abstractions.
- Watch for deprecations: if you plan to use a function/module, confirm it exists and isn’t marked `deprecated`/`TODO`/`FIXME`.
- Don’t commit secrets (`.env`, keys, credentials). If a script contains embedded secrets for tests, do not copy them into new locations.
- Keep PRs focused: smallest change that fixes the issue.

