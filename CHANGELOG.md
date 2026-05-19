# Changelog

## [1.0.0] — 2026-05-19

### Added
- FastAPI backend with async job queue for web and YouTube scraping
- Firecrawl Cloud API integration for web content extraction
- YouTube scraping via watch.py subprocess (asyncio.to_thread)
- Claude API outline generation (claude-sonnet-4-6) with prompt caching
- Structured markdown output with citation line and clickable source URL
- Title-slug file naming saved to outputs directory (PALANTIR_OUTPUTS_DIR configurable)
- React frontend with URL input, job status polling, outline viewer, history sidebar
- Copy to clipboard and download as .md for every outline
- Bearer token auth on all API routes (timing-safe hmac.compare_digest)
- Robots.txt compliance check before every scrape
- SQLite + SQLAlchemy (WAL mode) with pytest integration suite (10/10 passing)
- Pydantic field_validator rejects non-http/https URLs (returns 422)
- python-slugify sanitizes all filenames — path traversal blocked
- Teal accent (#00bcd4) applied to buttons, focus rings, and selected states
- Inline URL validation: empty submit and bad format shown as inline errors (no alerts)
- Accessible focus rings and aria-labels on all interactive elements
- Responsive layout: stacks at mobile (375px), splits at desktop (1024px+)

### Fixed
- Sync Anthropic client blocking async event loop → AsyncAnthropic
- Auth middleware was a pass no-op on all three route files → restored via shared auth.py
- Vite proxy targeting wrong backend port (8003 → 8008)
- YouTube subprocess blocking async context → asyncio.to_thread
- Web scraping using local mock content instead of real Firecrawl Cloud API
- CORS allowed origin was wrong port (5175 → 5180)
- PALANTIR_SECRET startup guard: raises RuntimeError if unset at startup
- storage.py OUTPUTS_DIR was hardcoded absolute path → env var + relative fallback
- storage.py mkdir deferred to write time (was at module import — crashed before any request)
- firecrawl.py silently returned mock content on any error → now raises properly
- youtube.py did not check WATCH_SCRIPTS_DIR env var → RuntimeError if unset
- JobStatus component catch block did not set error state → infinite spinner on network error
- OutlineHistory selected state and loading dots now use teal accent (were amber)
