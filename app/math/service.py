from supabase import Client
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
    GenerateProblemSetRequest,
    GenerateTestSetRequest,
    CompleteGeneratedQuestion,
    CompleteProblemSet,
    CompleteTestSet,
    MajorCategory,
    QuestionType,
    ModelVersion,
    SympySolvedQuestion,
    subcategory_data,
)
from typing import List
import random
import json

def generate_problems(
    data: GenerateSimilarQuestionRequest,
    supabase_exp: Client
) -> List[CompleteGeneratedQuestion]:
    question_count = data.question_count
    generated_questions = []
    category_questions = fetchSelectedQuestions(data.major_one_category, supabase_exp)
    for _ in range(question_count):
        example_question = random.choice(category_questions)
        generated_question = generate_sat_question(
            major_one_category=data.major_one_category,
            major_two_category=data.major_two_category,
            major_three_category=data.major_three_category,
            example_question=example_question,
            question_type=data.question_type,
        )
        
        solution_with_choices = solve_question(
            example_question=example_question,
            question_type=data.question_type,
        )
        # print(solution_with_choices)
        complete_generated_question_data = {
            **generated_question.dict(),
            **solution_with_choices.dict(),
        }
        complete_generated_question = CompleteGeneratedQuestion.parse_obj(
            complete_generated_question_data
        )

        # Convert the Pydantic model to a dictionary
        complete_generated_question_dict = complete_generated_question.dict()

        # Serialize the dictionary to a JSON string
        complete_generated_question_json = json.dumps(complete_generated_question_dict)
        data = supabase_exp.table("experiment_for_insertion").insert(complete_generated_question_json).execute()
        
        generated_questions.append(complete_generated_question)

    return generated_questions # return type: list of an instance of completeGeneratedQuestions.

def generate_problem_set(    
    data: GenerateProblemSetRequest,
    supabase_exp: Client
) -> List[CompleteProblemSet]:
    problem_count = data.question_count
    category = data.category

    problem_category_id_list = ProblemIdOfGivenCategories(category, supabase_exp)

    problems_ids = supabase_exp.table("problems").select("id, question, explanation").execute()
    problem_set = []
    problem_count = 2
    count = 0

    for category_id in problems_ids:
        for category_id_l in problem_category_id_list:
            if problem_count == count:
                break
            if category_id['id'] == category_id_l:
                if category_id not in problem_set:
                    problem_set.append(category_id)
                    count += 1
                    
    return problem_set

def fetchSelectedQuestions(category, supabase_exp):
    problem_category_id_list = ProblemIdOfGivenCategories(category, supabase_exp)

    problems_ids = supabase_exp.table("problems").select("id, question").execute()
    problems_ids_data = problems_ids.data
    questions = []

    for category_id in problems_ids_data:
        for category_id_l in problem_category_id_list:
            if category_id['id'] == category_id_l:
                if category_id not in questions:
                    questions.append(category_id)

    return questions

def ProblemIdOfGivenCategories(category, supabase_exp):
    
    problem_problem_categories_ids = supabase_exp.table("problem_problem_categories").select("problem_id, category_id").execute()
    problem_categories = supabase_exp.table("problem_categories").select("id, level1").execute()
    problem_problem_categories_ids_data = problem_problem_categories_ids.data
    problem_categories_data = problem_categories.data
    problem_category_id_list = []
    category_id_list = []

    for retrived_category in problem_categories_data:
        if retrived_category['level1'] == category:
            category_id_list.append(retrived_category['id'])

    
    for category_id in problem_problem_categories_ids_data:
        for category_id_l in category_id_list:
            if category_id['category_id'] == category_id_l:
                problem_category_id_list.append(category_id['problem_id'])

    return problem_category_id_list

def solve_sympy(question: str) -> SympySolvedQuestion:
    sympy_translation = translate_to_sympy(question)
    output = execute_expression(sympy_translation.sympy_expression)
    sympy_solved_question = make_explanation_by_sympy_expression(
        question=question,
        sympy_expression=sympy_translation.sympy_expression,
        output=output,
    )
    return sympy_solved_question