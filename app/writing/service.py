from writing.router import supabase
from fastapi import HTTPException
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
        complete_generated_question = CompleteGeneratedQuestion.parse_obj(
            generated_question.dict()
        )
        supabase.table("problems").insert(generated_question).execute()
        if generated_question.error:
            raise HTTPException(status_code=400, detail=generated_question.error.message)
        generated_questions.append(complete_generated_question)

    return generated_questions

def generate_problem_set(
    data: GenerateSimilarQuestionRequest,
) -> List[CompleteGeneratedQuestion]:
    question_set = []
    question_count = data.question_count
    for _ in range(question_count):
        question = supabase.table("problems").select("*").eq("question").execute()
        question_set.append(question)
    return question_set

def generate_test(
    data: GenerateSimilarQuestionRequest,
) -> List[CompleteGeneratedQuestion]:
    test_set = []

    return test_set