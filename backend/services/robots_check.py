from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse

def check(url: str) -> str:
    try:
        parsed = urlparse(url)
        robots_url = urljoin(f"{parsed.scheme}://{parsed.netloc}", "/robots.txt")
        rp = RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        allowed = rp.can_fetch("Palantir/1.0", url)
        return "allowed" if allowed else "disallowed"
    except Exception:
        return "unknown"
