# end points hit by user
# unique identifier
import uuid

# allows value o be none
from typing import Optional

# track timestamps
from datetime import datetime

# FastAPI endpoints, get dependencies, handle cookies, background tasks
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks

# session to interact with the database
from sqlalchemy.orm import Session

from db.database import get_db, SessionLocal
from models.story import Story, StoryNode
from models.job import StoryJob

# what the API expects or returns
from schemas.story import (
    CompleteStoryResponse,
    CompleteStoryNodeResponse,
    CreateStoryRequest,
)
from schemas.job import StoryJobResponse

# endpoint backend URL/api/stories/endpoint
router = APIRouter(prefix="/stories", tags=["stories"])


# get session id and identify browser
def get_session_id(session_id: Optional[str] = Cookie(None)):
    # if session does not exist create a new UUID
    if not session_id:
        # generate random uuid for session
        session_id = str(uuid.uuid4())
    return session_id


# define post endpoint at /stories/create
@router.post("/create", response_model=StoryJobResponse)
def create_story(
    # JSON body sent by the client to create a story
    request: CreateStoryRequest,
    # run long tasks async without blocking the response
    background_tasks: BackgroundTasks,
    # allows modifying headers, cookies
    response: Response,
    # calles you get_session_id function automatically
    session_id: str = Depends(get_session_id),
    # provides database session
    db: Session = Depends(get_db),
):
    # sends a cookie to the clients browser
    response.set_cookie(key="session_id", value=session_id, httponly=True)

    # create unique id for this story job
    job_id = str(uuid.uuid4())

    # create new instance
    job = StoryJob(
        job_id=job_id, session_id=session_id, theme=request.theme, status="pending"
    )
    # stage job
    db.add(job)
    # save into the database
    db.commit()

    # add background task and start running generate_story_task function
    background_tasks.add_task(
        generate_story_task, job_id=job_id, theme=request.theme, session_id=session_id
    )

    return job


# define background task style
def generate_story_task(job_id: str, theme: str, session_id: str):
    # make a new session
    db = SessionLocal()

    # get job from database
    try:
        # grab first entry from database
        job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()

        # if no job exist exit quietly
        if not job:
            return

        try:
            # updates job status
            job.status = "processing"
            # commit change
            db.commit()

            story = {}  # todo: generate story

            # hardcoded placeholder, mark job as completed
            job.story_id = 1  # todo: update story id
            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()
        # mark job as failed
        except Exception as e:
            job.status = "failed"
            job.completed_at = datetime.now()
            job.error = str(e)
            db.commit()
    # close database session
    finally:
        db.close()


# get story when it is finish
# registers a GET end point, story id taken from the path,
# FastAPI will serialize and validate he returned data against this Pydantic model.
@router.get("/{story_id}/complete", response_model=CompleteStoryResponse)
def get_complete_story(story_id: int, db: Session = Depends(get_db)):
    # Queries the Story table, filters by primary key(id)
    story = db.query(Story).filter(Story.id == story_id).first()
    # return 404 Not Found response, stops execution
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    complete_story = build_complete_story_tree(db, story)
    # returns SQLAlchemy Story object
    return complete_story


def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:
    pass
