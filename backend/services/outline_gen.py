import anthropic
import os
from datetime import datetime

_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")

SYSTEM_PROMPT = """You are a research assistant that converts scraped web/YouTube content into structured outlines.

Output a markdown document with this exact structure:
---
id: {id}
source_url: {url}
source_type: web | youtube
scraped_at: {timestamp}
robots_status: {robots_status}
model: claude-sonnet-4-6
---
# Outline: <Title>

*Scraped: YYYY-MM-DD at HH:MM UTC | Source: [domain.com](full_source_url)*

## Source Details
## Summary
## Key Topics
## Detailed Outline
## Operation Order / Task Breakdown
## Referenced URLs / Links
## Specs / Data / Numbers
## Video Timestamps (YouTube only)
## Raw Transcript Excerpt (YouTube only)
## Notes for AI Assistant

Rules:
- Be thorough but concise
- Hierarchical bullets for Detailed Outline
- Notes for AI Assistant: compact JSON-like block for Telegram bot
- If content is not a tutorial/process, omit Operation Order section
- For the citation line: format scraped_at as "YYYY-MM-DD at HH:MM UTC", use only the domain as the link text (e.g. pantheonmmo.com), and the full source URL as the href — e.g. *Scraped: 2026-05-19 at 14:58 UTC | Source: [pantheonmmo.com](https://www.pantheonmmo.com/game/classes/enchanter/)*"""

async def generate(url: str, source_type: str, raw_content: str, robots_status: str) -> str:
    client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    resp = await client.messages.create(
        model=_MODEL,
        max_tokens=4096,
        system=[{
            "type": "text",
            "text": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},
        }],
        messages=[{
            "role": "user",
            "content": f"URL: {url}\nSource type: {source_type}\nRobots status: {robots_status}\nScraped at: {datetime.utcnow().isoformat()}\n\n---CONTENT---\n{raw_content[:50000]}"
        }],
    )
    return resp.content[0].text
