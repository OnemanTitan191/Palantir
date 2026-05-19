import asyncio
import subprocess
import os

async def fetch(url: str) -> str:
    scripts_dir = os.getenv("WATCH_SCRIPTS_DIR")
    watch_py = os.path.join(scripts_dir, "watch.py")
    result = await asyncio.to_thread(
        subprocess.run,
        ["python", watch_py, url, "--no-whisper"],
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return result.stdout
