# SQLalchemy - ORM Object Relational Mapping
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base


class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    session_id = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # One to many relationship
    nodes = relationship("StoryNode", back_populates="story")


# metadata for the story
class StoryNode(Base):
    __tablename__ = "story_nodes"

    id = Column(Integer, primary_key=True, index=True)
    # store id of the story
    story_id = Column(Integer, ForeignKey("stories.id"), index=True)
    content = Column(String)
    # where to start story from
    is_root = Column(Boolean, default=False)
    # where to end story
    is_ending = Column(Boolean, default=False)
    # winning ending
    is_winning_ending = Column(Boolean, default=False)
    options = Column(JSON, default=list)
    # define relationship to story
    story = relationship("Story", back_populates="nodes")
