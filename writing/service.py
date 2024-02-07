from app.writing.utils import generate_sat_question
from app.writing.schemas import (
    GenerateSimilarQuestionRequest,
    CompleteGeneratedQuestion,
    Category,
    QuestionType,
    ModelVersion,
)
from typing import List


def generate_questions(
    data: GenerateSimilarQuestionRequest,
) -> List[CompleteGeneratedQuestion]:
    question_count = data.question_count
    generated_questions = []

    for _ in range(question_count):
        generated_question = generate_sat_question(
            category=data.category,
            example_question=data.example_question,
        )
        complete_generated_question = CompleteGeneratedQuestion.parse_obj(
            generated_question.dict()
        )
        generated_questions.append(complete_generated_question)

    return generated_questions


def get_category_list():
    return list(Category)


def get_question_type_list():
    return list(QuestionType)


def get_model_version_list():
    return list(ModelVersion)
