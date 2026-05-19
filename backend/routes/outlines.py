from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db
from models import Outline
import os

router = APIRouter()

def verify_token(authorization: str = Header(None)):
    secret = os.getenv("PALANTIR_SECRET")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if authorization.split(" ", 1)[1] != secret:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.get("/outlines")
def list_outlines(db: Session = Depends(get_db), _: None = Depends(verify_token)):
    outlines = db.query(Outline).all()
    return [
        {
            "id": o.id,
            "job_id": o.job_id,
            "title": o.title,
            "source_url": o.source_url,
            "source_type": o.source_type,
            "scraped_at": o.scraped_at.isoformat(),
            "robots_status": o.robots_status,
        }
        for o in outlines
    ]

@router.get("/outlines/{outline_id}")
def get_outline(outline_id: int, db: Session = Depends(get_db), _: None = Depends(verify_token)):
    outline = db.query(Outline).filter(Outline.id == outline_id).first()
    if not outline:
        raise HTTPException(status_code=404, detail="Outline not found")
    return {
        "id": outline.id,
        "job_id": outline.job_id,
        "title": outline.title,
        "source_url": outline.source_url,
        "source_type": outline.source_type,
        "scraped_at": outline.scraped_at.isoformat(),
        "robots_status": outline.robots_status,
        "md_content": outline.md_content,
        "file_path": outline.file_path,
    }

@router.get("/outlines/{outline_id}/download")
def download_outline(outline_id: int, db: Session = Depends(get_db), _: None = Depends(verify_token)):
    outline = db.query(Outline).filter(Outline.id == outline_id).first()
    if not outline:
        raise HTTPException(status_code=404, detail="Outline not found")
    return FileResponse(
        path=outline.file_path,
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="{outline.file_path.split(chr(92))[-1]}"'}
    )
