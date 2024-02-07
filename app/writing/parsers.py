from langchain.output_parsers import PydanticOutputParser
from app.math.schemas import (
    CompleteGeneratedQuestion,
)


complete_generated_question_parser = PydanticOutputParser(
    pydantic_object=CompleteGeneratedQuestion
)
