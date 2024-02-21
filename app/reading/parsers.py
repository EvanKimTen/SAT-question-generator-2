from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain.chat_models import ChatOpenAI
from app.constants import OPENAI_API_KEY

from app.reading.schemas import (
    GeneratedQuestion,
)

parser = PydanticOutputParser(pydantic_object=GeneratedQuestion)

generated_question_parser = OutputFixingParser.from_llm(
    parser=parser, llm=ChatOpenAI(openai_api_key=OPENAI_API_KEY)
)
