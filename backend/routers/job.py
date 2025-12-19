from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from models.job import StoryJob
from schemas.job import StoryJobResponse

# create FastAPI router to group related endpoints
router = APIRouter(prefix="/jobs", tags=["jobs"])


# GET job status based on job ID
# path parameter
@router.get("/{job_id}", response_model=StoryJobResponse)
# identify specific background job, injected via FastAPI dependency injection
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    # query the StoryJob table
    job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()
    # raise exception return 404
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # returns the SQLAlchemy model instance
    return job
