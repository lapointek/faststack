# interacting with the database
from sqlalchemy.orm import Session
from core.config import settings

# class to interact with OpenAI chat models
from langchain_openapi import ChatOpenAI

# define templates for the prompts
from langchain_core import PromptTemplate

# parse the models output into Pydantic models
from langchain_core.output_parsers import PydanticOutputParser

# prompt template
from core.prompts import STORY_PROMPT

# SQLAlchemy model representing the story table in the database
from models.story import Story
