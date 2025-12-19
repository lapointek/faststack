# interacting with the database
from sqlalchemy.orm import Session
from core.config import settings

# class to interact with OpenAI chat models
from langchain_openapi import ChatOpenAI

# define templates for the prompts
from langchain_core import ChatPromptTemplate

# parse the models output into Pydantic models
from langchain_core.output_parsers import PydanticOutputParser

# prompt template
from core.prompts import STORY_PROMPT

# SQLAlchemy model representing the story table in the database
from models.story import Story
from core.models import StoryLLMResponse, StoryNodeLLM


# defines a class to handle story generation logic
class StoryGenerator:
    @classmethod
    # private method
    def _get_llm(cls):
        return ChatOpenAI(model="gpt-4-turbo")

    # returns an instance of ChatOpenAI
    @classmethod
    # generate a story and save it into the database
    def generate_story(
        # SQLAlchemy Session for database operations,
        # Identifier for this story session, theme
        cls,
        db: Session,
        session_id: str,
        theme: str = "fantasy",
    ) -> Story:
        # get the LLM calls the private method
        llm = cls._get_llm()
        # ensures LLM ouput is parsed into the StoryLLMReponse Pydantic model
        story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)
        # creates a chat-style prompt with system instructions and user input
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", STORY_PROMPT),
                ("human", f"Create the story with this theme: {theme}"),
            ]
            # inserts the format instructions so the LLM knows to output JSON conforming to StoryLLMReponse
        ).partial(format_instructions=story_parser.get_format_instructions())

        # sends the prompt to the LLM and stores the response in raw_response
        raw_response = llm.invoke(prompt.invoke({}))

        # handles different response formats from the LLM
        response_text = raw_response
        if hasattr(raw_response, "content"):
            response_text = raw_response.content

        # converts the raw LLM output into a typed StoryLLMResponse object
        story_structure = story_parser.parse(response_text)

        # create a new Story object for the database
        story_db = Story(title=story_structure.title, session_id=session_id)
        # adds it to the session
        db.add(story_db)
        # ensures the object gets an ID immediately so you can link child nodes later
        db.flush()

        # convert dict from the LLM into a Pydantic StoryNodeLLM object using model_validate
        root_node_data = story_structure.rootNode
        if isinstance(root_node_data, dict):
            root_node_data = StoryNodeLLM.model_validate(root_node_data)

        # todo: process data

        db.commit()
        return story_db
