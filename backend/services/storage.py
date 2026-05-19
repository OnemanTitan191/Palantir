import os
from pathlib import Path
from datetime import datetime
from slugify import slugify


def _get_outputs_dir() -> Path:
    default = Path(__file__).resolve().parent.parent.parent / "outputs"
    return Path(os.getenv("PALANTIR_OUTPUTS_DIR", str(default)))


def _title_slug(md_content: str) -> str:
    for line in md_content.splitlines():
        if line.startswith("# Outline:"):
            title = line.replace("# Outline:", "").strip()
            return slugify(title, max_length=80)
    return ""


def write_md(url: str, md_content: str) -> Path:
    outputs_dir = _get_outputs_dir()
    outputs_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.utcnow().strftime("%Y-%m-%d")
    slug = _title_slug(md_content) or slugify(url, max_length=60)
    file_path = outputs_dir / f"{today}_{slug}.md"
    counter = 1
    while file_path.exists():
        file_path = outputs_dir / f"{today}_{slug}_{counter}.md"
        counter += 1
    try:
        file_path.write_text(md_content, encoding="utf-8")
    except OSError as e:
        raise RuntimeError(f"Failed to write outline to {file_path}: {e}") from e
    return file_path
