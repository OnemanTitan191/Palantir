import httpx
import os

async def fetch(url: str) -> str:
    use_mock = os.getenv("USE_MOCK_FIRECRAWL", "true").lower() == "true"
    if use_mock:
        return _mock_content(url)

    api_url = os.getenv("FIRECRAWL_API_URL", "http://localhost:3002")
    api_key = os.getenv("FIRECRAWL_API_KEY", "test-key-local-dev")
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            f"{api_url}/v1/scrape",
            json={"url": url, "formats": ["markdown"]},
            headers={"Authorization": f"Bearer {api_key}"}
        )
        resp.raise_for_status()
        data = resp.json()
        content = data.get("data", {}).get("markdown", "")
    if not content.strip():
        raise RuntimeError(f"Firecrawl returned empty content for {url}")
    return content

def _mock_content(url: str) -> str:
    return f"""# Content from {url}

## Overview
This is mock content for testing. The actual Firecrawl service is unavailable.
Real scraping will work once Firecrawl Docker container is running.

## Key Sections
- Introduction to the topic
- Main concepts and ideas
- Practical applications
- References and links

## Details
URL: {url}
Source Type: web
Status: Mock data (for testing)

This placeholder content demonstrates the outline generation pipeline.
Replace with real Firecrawl when the service is available."""
