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
    GeneratedQuestion,
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
    supabase: Client
) -> List[CompleteGeneratedQuestion]:
    question_count = data.question_count
    generated_questions = []
    category_questions = fetchSelectedQuestions(data.major_one_category, supabase)
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
        data = supabase.table("experiment_for_insertion").insert(complete_generated_question_json).execute()
        
        generated_questions.append(complete_generated_question)

    return generated_questions # return type: list of an instance of completeGeneratedQuestions.

def generate_problem_set(    
    data: GenerateProblemSetRequest,
    supabase: Client
) -> CompleteProblemSet:
    problem_count = data.question_count
    category = data.category

    problem_category_id_list = ProblemIdOfGivenCategories(category, supabase)

    problems_ids = supabase.table("problems").select("id, question, explanation").execute()
    problems_ids_data = problems_ids.data
    problem_set = []
    problem_count = 2
    count = 0
    for problems_id in problems_ids_data:
        for problem_category_id in problem_category_id_list:
            if problem_count == count:
                break
            if problems_id["id"] == problem_category_id:
                if problems_id not in problem_set:
                    problem_set.append(problems_id)
                    count += 1
    
    list_prob_set = []
    for problem in problem_set:
        complete_generated_question = GeneratedQuestion.parse_obj(
            problem
        )
        list_prob_set.append(complete_generated_question)
    complete_problem_set = CompleteProblemSet(
        name="New Problem Set",
        is_full_test=False,
        # user_id=12,
        set=list_prob_set 
    )
    complete_problem_set_dict = complete_problem_set.dict()
    print(complete_problem_set_dict)
    data = supabase.table("exp_insertion_problem_set").insert(complete_problem_set_dict).execute()
    return complete_problem_set

def fetchSelectedQuestions(category, supabase):
    problem_category_id_list = ProblemIdOfGivenCategories(category, supabase)

    problems_ids = supabase.table("problems").select("id, question").execute()
    problems_ids_data = problems_ids.data
    questions = []

    for category_id in problems_ids_data:
        for category_id_l in problem_category_id_list:
            if category_id['id'] == category_id_l:
                if category_id not in questions:
                    questions.append(category_id)

    return questions

def ProblemIdOfGivenCategories(category, supabase):
    
    problem_problem_categories_ids = supabase.table("problem_problem_categories").select("problem_id, category_id").execute()
    problem_categories = supabase.table("problem_categories").select("id, level1").execute()
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
    output = executeression(sympy_translation.sympyression)
    sympy_solved_question = makelanation_by_sympyression(
        question=question,
        sympyression=sympy_translation.sympyression,
        output=output,
    )
    return sympy_solved_question