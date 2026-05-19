# Palantír — Content Scraper & Outline Generator

A LotR-themed web and YouTube content scraper. Paste any URL → backend scrapes it (Firecrawl for web, watch.py for YouTube) → Claude API generates a structured outline → saved to disk as `.md` and indexed in SQLite.

## Purpose

Fast conversion of any research URL (Kia tech videos, coding tutorials) into a referenceable structured outline — usable manually or forwarded to an AI assistant via Telegram.

## Tech Stack

- **Backend:** FastAPI + Python 3.11+
- **Frontend:** Vite + React + TypeScript + Tailwind CSS
- **Database:** SQLite + SQLAlchemy (WAL mode)
- **Web Scraping:** Firecrawl Cloud API (`https://api.firecrawl.dev`)
- **YouTube:** watch.py subprocess integration
- **LLM:** Claude API (claude-sonnet-4-6) with prompt caching
- **Auth:** Bearer token (PALANTIR_SECRET)

## Architecture

```
[Minas Tirith :3000] → [Palantir Frontend :5180]
                             ↓ (REST API)
                     [Palantir Backend :8008]
                         ↙ web  ↘ youtube
               Firecrawl Cloud   watch.py
                         ↘ ↙
                   Claude API → Structured Outline
                         ↓
                   SQLite + /outputs/*.md
```

## Setup

### 1. Prerequisites

- Python 3.11+
- Node.js + npm
- [Firecrawl Cloud API key](https://firecrawl.dev) (free tier available)
- Anthropic API key

### 2. Backend Setup

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` to `.env` (one directory up, at the palantir root) and fill in your keys:
```
ANTHROPIC_API_KEY=sk-ant-...
PALANTIR_SECRET=your-secret-here
FIRECRAWL_API_URL=https://api.firecrawl.dev
FIRECRAWL_API_KEY=fc-...
USE_MOCK_FIRECRAWL=false
WATCH_SCRIPTS_DIR=C:\Users\yourname\.claude\skills\watch\scripts
```

### 3. Frontend Setup

```powershell
cd frontend
npm install
```

Create `frontend/.env`:
```
VITE_PALANTIR_SECRET=your-secret-here
```

## Running

### Terminal 1 — Backend

```powershell
cd backend
.venv\Scripts\Activate.ps1
uvicorn main:app --host 127.0.0.1 --port 8008 --reload
```

### Terminal 2 — Frontend

```powershell
cd frontend
npm run dev -- --port 5180
```

### Terminal 3 — Minas Tirith (Gateway, optional)

```powershell
cd ../minas-tirith
npm run dev
```

## API Endpoints

**Health Check:**
```
GET /health
```

**Scrape a URL (web or YouTube):**
```
POST /api/scrape
Authorization: Bearer {PALANTIR_SECRET}
Body: { "url": "https://example.com" }
Response: { "job_id": 1, "status": "pending" }
```

**Get Job Status:**
```
GET /api/jobs/{job_id}
Authorization: Bearer {PALANTIR_SECRET}
```

**List All Jobs:**
```
GET /api/jobs
Authorization: Bearer {PALANTIR_SECRET}
```

**List All Outlines:**
```
GET /api/outlines
Authorization: Bearer {PALANTIR_SECRET}
```

**Get Outline:**
```
GET /api/outlines/{outline_id}
Authorization: Bearer {PALANTIR_SECRET}
```

**Download Outline as Markdown:**
```
GET /api/outlines/{outline_id}/download
Authorization: Bearer {PALANTIR_SECRET}
```

## Database

SQLite database at `data/palantir.db` (auto-created on first startup).

**Tables:**
- `jobs` — scraping task records (status, URL, timestamps)
- `outlines` — generated outlines (title, source, markdown content, file path)

## Output

Generated markdown files are saved to the configured `PALANTIR_OUTPUTS_DIR` (defaults to `BarahdurVault/04 Archive/Palantir/`) with naming pattern:
```
YYYY-MM-DD_{title-slug}.md
```

Each outline includes a citation line linking back to the source:
```
*Scraped: 2026-05-19 at 14:58 UTC | Source: [example.com](https://example.com/page)*
```

## Design Tokens

**Colors:**
- Background: #0d0d0d
- Surface: #1a1a2e
- Text: #e8e8f0
- Accent: #c4963e (amber gold)

**Font:** Cinzel (serif)

**UI Copy:**
- Title: "THE PALANTÍR — See All, Know All"
- Input: "Place a URL in the stone..."
- Submit: "Gaze Into the Stone"
- Processing: "The Eye searches..." → "The stone reveals..."

## Stages

- **Stage 0** ✅ — Foundation (directory structure, venv, frontend scaffold)
- **Stage 1** ✅ — Backend MVP (FastAPI, SQLAlchemy, services, routes)
- **Stage 2** ✅ — Debug & Testing (AsyncAnthropic, auth, proxy port, subprocess, Firecrawl wiring; 4/4 tests passing)
- **Stage 3** — Quality Check
- **Stage 4** — Advanced UI
- **Stage 5** — Finalize
- **Stage 6** ✅ — Push to GitHub

## Notes

- Prompt caching enabled on Claude system prompt for cost savings
- robots.txt compliance checked before every scrape
- All API requests require Bearer token authentication
- Background tasks process scrapes asynchronously
- YouTube scrapes use `asyncio.to_thread()` to avoid blocking the event loop
