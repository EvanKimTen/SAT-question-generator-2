from math.router import supabase
from fastapi import HTTPException
from app.math.utils import (
    generate_sat_question,
    solve_question,
    translate_to_sympy,
    make_explanation_by_sympy_expression,
    execute_expression,
)
from app.math.schemas import (
    GenerateSimilarQuestionRequest,
    CompleteGeneratedQuestion,
    MajorCategory,
    QuestionType,
    ModelVersion,
    SympySolvedQuestion,
    subcategory_data,
)
from typing import List


def generate_questions(
    data: GenerateSimilarQuestionRequest,
) -> List[CompleteGeneratedQuestion]:
    question_count = data.question_count
    generated_questions = []

    for _ in range(question_count):
        generated_question = generate_sat_question(
            major_one_category=data.major_one_category,
            major_two_category=data.major_two_category,
            sub_one_category=data.sub_one_category,
            sub_two_category=data.sub_two_category,
            example_question=data.example_question,
            question_type=data.question_type,
        )
        solution_with_choices = solve_question(
            example_question=generated_question.question,
            question_type=data.question_type,
        )
        complete_generated_question_data = {
            **generated_question.dict(),
            **solution_with_choices.dict(),
        }
        complete_generated_question = CompleteGeneratedQuestion.parse_obj(
            complete_generated_question_data
        )
        supabase.table("problems").insert(complete_generated_question).execute()
        if complete_generated_question.error:
            raise HTTPException(status_code=400, detail=generated_question.error.message)
        generated_questions.append(complete_generated_question)

    return generated_questions

def generate_problem_set(    
    data: GenerateSimilarQuestionRequest,
) -> List[CompleteGeneratedQuestion]:
    question_count = data.question_count
    question_set = []
    for _ in range(question_count):
        question = supabase.table("problems").select("*").eq("question").execute() # will modify soon once
        # grasp a gist of the db contents.
        question_set.append(question)

    return question_set

def generate_test_set(    
    data: GenerateSimilarQuestionRequest,
) -> List[CompleteGeneratedQuestion]:
    question_count = data.question_count
    question_set = []

    for _ in range(question_count):
        question_set.append(data.example_question)

    return question_set

def solve_sympy(question: str) -> SympySolvedQuestion:
    sympy_translation = translate_to_sympy(question)
    output = execute_expression(sympy_translation.sympy_expression)
    sympy_solved_question = make_explanation_by_sympy_expression(
        question=question,
        sympy_expression=sympy_translation.sympy_expression,
        output=output,
    )
    return sympy_solved_question