# CLAUDE.md — Palantir

## Purpose
LotR-themed web and YouTube content scraper. Paste any URL → backend scrapes it → Claude API generates a structured outline → saved as `.md` and indexed in SQLite.

## Quick Start
```powershell
# Backend (port 8008)
cd projects/palantir/backend
.venv\Scripts\Activate.ps1
uvicorn main:app --host 127.0.0.1 --port 8008 --reload

# Frontend (port 5180)
cd projects/palantir/frontend
npm run dev
```

Browser: http://localhost:5180

**No Docker required** — uses Firecrawl Cloud API, not self-hosted.

## Architecture
- Backend: FastAPI, port 8008 — routes in `backend/routes/`
- Frontend: React + Vite + TypeScript + Tailwind, port 5180
- Database: SQLite at `backend/data/palantir.db` — backup before schema changes
- Web scraping: Firecrawl Cloud API (`https://api.firecrawl.dev`)
- YouTube: `watch.py` subprocess integration
- LLM: Claude API (model from `.env`) with prompt caching
- Auth: Bearer token (PALANTIR_SECRET) — NEVER disable

## CRITICAL: Async Rules
- ALWAYS use `anthropic.AsyncAnthropic` — NEVER the sync client in `async def` functions
- YouTube subprocess: ALWAYS use `asyncio.to_thread()` — never call blocking subprocess directly in async
- Robots check: ALWAYS use `asyncio.to_thread()` for blocking HTTP calls

## Required .env Variables
```
PALANTIR_SECRET=<your-secret>
ANTHROPIC_API_KEY=<your-key>
ANTHROPIC_MODEL=claude-sonnet-4-6
FIRECRAWL_API_KEY=<your-key>
FIRECRAWL_API_URL=https://api.firecrawl.dev
WATCH_SCRIPTS_DIR=<path-to-watch.py-scripts>
```

## Security Notes
- Path traversal hardened in `storage.py` via python-slugify
- URL injection guarded by Pydantic `field_validator` (rejects non-http/https)
- PALANTIR_SECRET uses `hmac.compare_digest` for timing-safe comparison

## Current Stage
Stage 6 complete — shipped to GitHub. See `BarahdurVault/01 Projects/WIP/Palantir/Overview.md`.
