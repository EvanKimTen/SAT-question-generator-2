from writing.router import supabase
from fastapi import HTTPException
from app.writing.schemas import (
    GenerateSimilarQuestionRequest,
    CompleteGeneratedQuestion,
    CompleteProblemSet,
    TestQuestionRequest,
    CompleteTestSet,
)

from app.writing.utils import generate_sat_question

from typing import List
import random

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
) -> List[CompleteProblemSet]:
    question_set = []
    question_count = data.question_count
    for _ in range(question_count):
        question = supabase.table("problems").select("*").eq("question").execute()
        question_set.append(question)
    return question_set

def generate_test(
    data: TestQuestionRequest,
) -> List[CompleteTestSet]:
    test_set = []
    total_questions = data.question_count
    category_distribution = {
        "Craft & Structure" : 0.28,
        "Information & Ideas": 0.26,
        "Conventions Of Standard English": 0.26,
        "Expression of Ideas": 0.20
    }
    modules = supabase.table("test_problems").select("module").execute() 
    # More details needed for getting different module individually.

    for module in modules:
        if module == "1":
            category_distribution = {
                "Craft & Structure" : 0.28, #
                "Relevant Information": 0.26,
                "Conventions Of Standard English": 0.26,
                "Most Logical Transition": 0.20
            }
            for category, ratio in category_distribution.items():
                category_questions, num_questions_to_select = randomlySelectProblems(category, ratio, total_questions)
                test_set.extend(random.sample(category_questions, num_questions_to_select))

        elif module == "2-easy":
            category_distribution = {
                "Craft & Structure" : 0.28,
                "Information & Ideas": 0.26,
                "Conventions Of Standard English": 0.26,
                "Expression of Ideas": 0.20
            }
            for category, ratio in category_distribution.items():
                category_questions, num_questions_to_select = randomlySelectProblems(category, ratio, total_questions)
                test_set.extend(random.sample(category_questions, num_questions_to_select))

        elif module == "2-hard":
            category_distribution = {
                "Craft & Structure" : 0.28,
                "Information & Ideas": 0.26,
                "Conventions Of Standard English": 0.26,
                "Expression of Ideas": 0.20
            }
            for category, ratio in category_distribution.items():
                category_questions, num_questions_to_select = randomlySelectProblems(category, ratio, total_questions)
                test_set.extend(random.sample(category_questions, num_questions_to_select))
    return test_set

def randomlySelectProblems(category, ratio, total_questions):
    num_questions_to_select = round(total_questions * ratio)
    query = f"""
    SELECT problems.question
    FROM problems
    INNER JOIN problem_problem_categories ON problem_problem_categories.category_id = problems.id
    INNER JOIN problem_categories ON problem_problem_categories.category_id = problem_categories.id
    WHERE problem_categories.level2 = '{category}'
    """
    category_questions = supabase.table("problems").execute_sql(query)
    return num_questions_to_select, category_questions

    

                