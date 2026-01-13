# interacting with the database
from sqlalchemy.orm import Session

# class to interact with OpenAI chat models
from langchain_openai import ChatOpenAI

# define templates for the prompts
from langchain_core.prompts import ChatPromptTemplate

# parse the models output into Pydantic models
from langchain_core.output_parsers import PydanticOutputParser

# prompt template
from core.prompts import STORY_PROMPT

# SQLAlchemy model representing the story table in the database
from models.story import Story, StoryNode
from core.models import StoryLLMResponse, StoryNodeLLM
from dotenv import load_dotenv
import os

load_dotenv()


# defines a class to handle story generation logic
class StoryGenerator:
    @classmethod
    def _get_llm(cls):
        return ChatOpenAI(
            model="gpt-4o-mini",
        )

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
        # has attribute
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

        cls._process_story_node(db, story_db.id, root_node_data, is_root=True)

        db.commit()
        return story_db

    @classmethod
    def _process_story_node(
        cls, db: Session, story_id: int, node_data: StoryNodeLLM, is_root: bool = False
    ) -> StoryNode:
        # create database StoryNode
        node = StoryNode(
            # link node to its Story
            story_id=story_id,
            # extract node content safely
            content=(
                node_data.content
                if hasattr(node_data, "content")
                else node_data["content"]
            ),
            # whether this is the root node
            is_root=is_root,
            # determine if ending node
            is_ending=(
                node_data.isEnding
                if hasattr(node_data, "isEnding")
                else node_data["isEnding"]
            ),
            # determine if winning ending
            is_winning_ending=(
                node_data.isWinningEnding
                if hasattr(node_data, "isWinningEnding")
                else node_data["isWinningEnding"]
            ),
            # initialize options
            options=[],
        )
        # add node to database
        db.add(node)
        # ensures node.id exists before you attach child nodes or options
        db.flush()

        # check if the node can have children
        if not node.is_ending and (hasattr(node_data, "options") and node_data.options):
            # store options
            options_list = []
            # loop through each story option
            for option_data in node_data.options:
                next_node = option_data.nextNode
                # extract and validate the next node
                if isinstance(next_node, dict):
                    next_node = StoryNodeLLM.model_validate(next_node)
                # recursively create the child node
                # false indicates this is not the root node
                child_node = cls._process_story_node(db, story_id, next_node, False)

                # option text shown to the player
                options_list.append(
                    {
                        "text": option_data.text,
                        "node_id": child_node.id,
                    }
                )
                # attach options to the current node
            node.options = options_list

        db.flush()
        # return fully-processed node
        return node
