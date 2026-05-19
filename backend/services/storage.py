import os
from pathlib import Path
from datetime import datetime
from slugify import slugify

_default = r"C:\Users\tanne\Documents\BarahdurVault\04 Archive\Palantir"
OUTPUTS_DIR = Path(os.getenv("PALANTIR_OUTPUTS_DIR", _default))
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

def _title_slug(md_content: str) -> str:
    for line in md_content.splitlines():
        if line.startswith("# Outline:"):
            title = line.replace("# Outline:", "").strip()
            return slugify(title, max_length=80)
    return ""

def write_md(url: str, md_content: str) -> Path:
    today = datetime.utcnow().strftime("%Y-%m-%d")
    slug = _title_slug(md_content) or slugify(url, max_length=60)
    file_path = OUTPUTS_DIR / f"{today}_{slug}.md"
    file_path.write_text(md_content, encoding="utf-8")
    return file_path
