# schemas is the structure for the data
from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel


# one choice/option the user can select
class StoryOptionsSchema(BaseModel):
    # label shown to the user
    text: str
    # id of the next story node
    node_id: Optional[int] = None


# reuse these fields in multiple schemas
class StoryNodeBase(BaseModel):
    # the story text shown to the player
    content: str
    # marks whether this node ends the story
    is_ending: bool = False
    # indicates a successful ending
    is_winning_ending: bool = False


# response from API represents full story node returned
# inherits everything from the StoryNodeBase
class CompleteStoryNodeResponse(StoryNodeBase):
    # unique identifier
    id: int
    # list of choices available from this node
    options: List[StoryOptionsSchema] = []

    # create model from the ORM
    class Config:
        from_attributes = True


# represents shared fields for a story
class StoryBase(BaseModel):
    # stories title
    title: str
    # associate story with user session
    session_id: Optional[str] = None

    # create model from ORM object
    class Config:
        from_attributes = True


# represents the request body when creating a story
class CreateStoryRequest(BaseModel):
    theme: str


# full story returned by the API
class CompleteStoryResponse(StoryBase):
    # database id for the story
    id: int
    # timestamp of creation
    created_at: datetime
    # starting node of the story
    root_node: CompleteStoryNodeResponse
    # lookup table for every node in the story
    all_nodes: Dict[int, CompleteStoryNodeResponse]

    # create model from ORM object
    class Config:
        from_attributes = True
