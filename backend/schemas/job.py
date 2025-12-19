from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class StoryJobBase(BaseModel):
    # theme for the created job
    theme: str


class StoryJobResponse(BaseModel):
    # unique identifier for the background job
    job_id: int
    # job lifecycle state
    status: str
    # job was created
    created_at: datetime
    # set when job completes successfully
    story_id: Optional[int] = None
    # timestamp when job finished success or failure
    completed_at = Optional[datetime] = None
    # error message if the job fails
    error: Optional[str] = None

    class Config:
        from_attributes = True


class StoryJobCreate(StoryJobBase):
    pass
