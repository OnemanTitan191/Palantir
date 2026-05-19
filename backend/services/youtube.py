import asyncio
import subprocess
import os

async def fetch(url: str) -> str:
    scripts_dir = os.getenv("WATCH_SCRIPTS_DIR")
    if not scripts_dir:
        raise RuntimeError("WATCH_SCRIPTS_DIR env var is not set")
    watch_py = os.path.join(scripts_dir, "watch.py")
    result = await asyncio.to_thread(
        subprocess.run,
        ["python", watch_py, url, "--no-whisper"],
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or "watch.py exited with non-zero status")
    if not result.stdout.strip():
        raise RuntimeError("watch.py returned empty transcript")
    return result.stdout
