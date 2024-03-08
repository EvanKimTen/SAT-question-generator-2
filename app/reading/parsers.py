from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain.chat_models import ChatOpenAI
from app.reading.schemas import (
    GeneratedQuestion,
    PreprocessedPassage,
)
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

parser = PydanticOutputParser(pydantic_object=GeneratedQuestion)

generated_question_parser = OutputFixingParser.from_llm(
    parser=parser, llm=ChatOpenAI(openai_api_key=OPENAI_API_KEY)
)

preprocessed_passage_parser = PydanticOutputParser(pydantic_object=PreprocessedPassage)
