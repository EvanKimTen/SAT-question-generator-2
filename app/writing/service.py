from app.writing.schemas import (
    GenerateSimilarQuestionRequest,
    CompleteGeneratedQuestion,
)

from app.writing.utils import generate_sat_question

from typing import List

def generate_questions(
    data: GenerateSimilarQuestionRequest,
) -> List[CompleteGeneratedQuestion]:
# process parameter to send back in the form of CompleteGeneratedQuestion.
    question_count = data.question_count
    generated_questions = []

    for _ in range(question_count):
        generated_question = generate_sat_question(
            category=data.category,
            example_question=data.example_question,
        )
        complete_generated_question = CompleteGeneratedQuestion.model_validate(
            generated_question.dict()
        )
        generated_questions.append(complete_generated_question)

    return generated_questions
        