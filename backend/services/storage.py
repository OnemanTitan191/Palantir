import os
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
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


def _domain(url: str) -> str:
    try:
        return urlparse(url).netloc or url
    except Exception:
        return url


def write_md(url: str, md_content: str) -> tuple[str, Path]:
    outputs_dir = _get_outputs_dir()
    outputs_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.utcnow()
    date_str = now.strftime("%Y_%m_%d")
    slug = _title_slug(md_content) or slugify(url, max_length=60)
    file_stem = f"{date_str}_{slug}"
    file_path = outputs_dir / f"{file_stem}.md"
    counter = 1
    while file_path.exists():
        file_path = outputs_dir / f"{file_stem}_{counter}.md"
        counter += 1

    dt_str = now.strftime("%Y-%m-%d %H:%M UTC")
    new_title = f"# {file_path.stem} | {dt_str} | [{_domain(url)}]({url})"

    lines = md_content.splitlines()
    modified_lines = []
    replaced = False
    for line in lines:
        if not replaced and line.startswith("# Outline:"):
            modified_lines.append(new_title)
            replaced = True
        else:
            modified_lines.append(line)
    if not replaced:
        modified_lines.insert(0, new_title)
    modified_content = "\n".join(modified_lines)

    try:
        file_path.write_text(modified_content, encoding="utf-8")
    except OSError as e:
        raise RuntimeError(f"Failed to write outline to {file_path}: {e}") from e
    return modified_content, file_path
