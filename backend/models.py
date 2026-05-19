from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    url: Mapped[str] = mapped_column(String, nullable=False)
    source_type: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    error_msg: Mapped[str | None] = mapped_column(Text, nullable=True)
    outline: Mapped["Outline"] = relationship("Outline", back_populates="job", uselist=False)

class Outline(Base):
    __tablename__ = "outlines"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_id: Mapped[int] = mapped_column(Integer, ForeignKey("jobs.id"))
    title: Mapped[str] = mapped_column(String)
    source_url: Mapped[str] = mapped_column(String)
    source_type: Mapped[str] = mapped_column(String)
    scraped_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    robots_status: Mapped[str] = mapped_column(String)
    md_content: Mapped[str] = mapped_column(Text)
    file_path: Mapped[str] = mapped_column(String)
    job: Mapped["Job"] = relationship("Job", back_populates="outline")
