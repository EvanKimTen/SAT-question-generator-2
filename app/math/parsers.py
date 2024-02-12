from langchain.output_parsers import PydanticOutputParser
from app.math.schemas import (
    GeneratedQuestion,
    SolutionWithChoices,
    CompleteGeneratedQuestion,
    SympyTranslation,
    SympySolvedQuestion,
)


generated_question_parser = PydanticOutputParser(pydantic_object=GeneratedQuestion)

solution_with_choices_parser = PydanticOutputParser(pydantic_object=SolutionWithChoices)

complete_generated_question_parser = PydanticOutputParser(
    pydantic_object=CompleteGeneratedQuestion
)

sympy_translation_parser = PydanticOutputParser(pydantic_object=SympyTranslation)

sympy_solved_question_parser = PydanticOutputParser(pydantic_object=SympySolvedQuestion)
