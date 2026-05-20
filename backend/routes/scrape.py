import asyncio
from datetime import datetime

from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session

from auth import verify_token
from database import get_db, SessionLocal
from models import Job, Outline
from services import firecrawl, youtube, outline_gen, storage, robots_check

router = APIRouter()


class ScrapeRequest(BaseModel):
    url: str

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        if not v.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")
        return v


@router.post("/scrape")
async def scrape(
    body: ScrapeRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _: None = Depends(verify_token),
):
    url = body.url
    source_type = "youtube" if ("youtube.com" in url or "youtu.be" in url) else "web"
    job = Job(url=url, source_type=source_type, status="pending")
    db.add(job)
    db.commit()
    db.refresh(job)
    background_tasks.add_task(process_job, job.id, url, source_type)
    return {"job_id": job.id, "status": "pending"}


async def process_job(job_id: int, url: str, source_type: str):
    db = SessionLocal()
    job = None
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return
        job.status = "running"
        db.commit()

        robots = await asyncio.to_thread(robots_check.check, url)
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
        title = extract_title(outline_md)
        modified_content, file_path = storage.write_md(url, outline_md)

        outline = Outline(
            job_id=job_id, title=title,
            source_url=url, source_type=source_type,
            scraped_at=datetime.utcnow(), robots_status=robots,
            md_content=modified_content, file_path=str(file_path),
        )
        db.add(outline)
        job.status = "done"
        job.completed_at = datetime.utcnow()
        db.commit()
    except Exception as e:
        db.rollback()
        _job = db.query(Job).filter(Job.id == job_id).first()
        if _job:
            _job.status = "error"
            _job.error_msg = str(e)
            db.commit()
    finally:
        db.close()


def extract_title(md: str) -> str:
    for line in md.splitlines():
        if line.startswith("# Outline:"):
            return line.replace("# Outline:", "").strip()
    return "Untitled"
