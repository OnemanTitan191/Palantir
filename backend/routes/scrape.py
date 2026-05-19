from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_db
from models import Job, Outline
from services import firecrawl, youtube, outline_gen, storage, robots_check
from datetime import datetime
import os

router = APIRouter()

def verify_token(authorization: str = Header(None)):
    secret = os.getenv("PALANTIR_SECRET")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if authorization.split(" ", 1)[1] != secret:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.post("/scrape")
async def scrape(
    body: dict,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _: None = Depends(verify_token),
):
    url: str = body["url"]
    source_type = "youtube" if ("youtube.com" in url or "youtu.be" in url) else "web"
    job = Job(url=url, source_type=source_type, status="pending")
    db.add(job)
    db.commit()
    db.refresh(job)
    background_tasks.add_task(process_job, job.id, url, source_type)
    return {"job_id": job.id, "status": "pending"}

async def process_job(job_id: int, url: str, source_type: str):
    from database import SessionLocal
    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        job.status = "running"
        db.commit()

        robots = robots_check.check(url)
        if robots == "disallowed":
            job.status = "error"
            job.error_msg = "The stone has been barred. (robots.txt blocks this URL)"
            db.commit()
            return

        if source_type == "youtube":
            raw_content = await youtube.fetch(url)
        else:
            raw_content = await firecrawl.fetch(url)

        outline_md = await outline_gen.generate(url, source_type, raw_content, robots)
        file_path = storage.write_md(url, outline_md)

        outline = Outline(
            job_id=job_id, title=extract_title(outline_md),
            source_url=url, source_type=source_type,
            scraped_at=datetime.utcnow(), robots_status=robots,
            md_content=outline_md, file_path=str(file_path),
        )
        db.add(outline)
        job.status = "done"
        job.completed_at = datetime.utcnow()
        db.commit()
    except Exception as e:
        job.status = "error"
        job.error_msg = str(e)
        db.commit()
    finally:
        db.close()

def extract_title(md: str) -> str:
    for line in md.splitlines():
        if line.startswith("# Outline:"):
            return line.replace("# Outline:", "").strip()
    return "Untitled"
