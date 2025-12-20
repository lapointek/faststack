# type hints from Pythons typing module
from typing import List, Dict, Any, Optional

# Python library for data validation and management using type hints
from pydantic import BaseModel, Field


# option that players choose in the story
class StoryOptionLLM(BaseModel):
    # text displayed for this option
    text: str = Field(description="the text of the option shown to the user")
    # dictionary representing the next story node
    nexNode: Dict[str, Any] = Field(description="the next node content and its options")


# node in the story
class StoryNodeLLM(BaseModel):
    # text conent of this part of the story
    content: str = Field(description="The main content of the story node")
    isEnding: bool = Field(description="Whether this node is an ending node")
    isWinningEnding: bool = Field(
        description="Whether this node is a winning ending node"
    )
    # list of StoryOptionLLm objects representing choices the player can make
    options: Optional[List[StoryOptionLLM]] = Field(
        default=None, description="The options for this node"
    )


# represents the entire story returned from LLM
class StoryLLMResponse(BaseModel):
    title: str = Field(description="The title of the story")
    # starting point of the story (StoryNodeLLM) from which the player
    # can start navigating through the options
    rootNode: StoryNodeLLM = Field(description="The root node of the story")
