from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import verify_token
from database import get_db
from models import Job

router = APIRouter()


@router.get("/jobs")
def list_jobs(db: Session = Depends(get_db), _: None = Depends(verify_token)):
    jobs = db.query(Job).all()
    return [
        {
            "id": j.id,
            "url": j.url,
            "source_type": j.source_type,
            "status": j.status,
            "created_at": j.created_at.isoformat(),
            "completed_at": j.completed_at.isoformat() if j.completed_at else None,
            "error_msg": j.error_msg,
        }
        for j in jobs
    ]


@router.get("/jobs/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db), _: None = Depends(verify_token)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "id": job.id,
        "url": job.url,
        "source_type": job.source_type,
        "status": job.status,
        "created_at": job.created_at.isoformat(),
        "completed_at": job.completed_at.isoformat() if job.completed_at else None,
        "error_msg": job.error_msg,
    }
