from supabase import Client
from fastapi import HTTPException, Header
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
    supabase: Client,
    access_token: str,
    refresh_token: str,
) -> List[CompleteGeneratedQuestion]:
    supabase.auth.set_session(access_token, refresh_token)
    user_id = supabase.auth.get_user().user.id

    generated_questions = []
    question_count = data.question_count
    question_type = data.question_type
    list_major_categories = []
    if data.first_level_2 is not None:
        list_major_categories.append([data.first_level_1, data.first_level_2])
    if data.second_level_2 is not None:
        list_major_categories.append([data.second_level_1, data.second_level_2])
    if data.third_level_2 is not None:
        list_major_categories.append([data.third_level_1, data.third_level_2])

    for _ in range(question_count):
        major_category = random.choice(list_major_categories)
        lv1_major_category = major_category[0]
        lv2_major_category = major_category[1]
        category_questions = fetchSelectedQuestions(lv1_major_category, lv2_major_category, supabase)
        example_question = random.choice(category_questions)
        generated_question = generate_sat_question(
            major_category=major_category,
            example_question=example_question,
            question_type=question_type,
        )
        solution_with_choices = solve_question(
            example_question=example_question,
            question_type=question_type,
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
        passage_dict = {'passage': None}
        complete_generated_question_dict = passage_dict | complete_generated_question_dict
        complete_generated_question_dict['user_id'] = user_id
        data = supabase.table("exp_insertion_problem_gen").insert(complete_generated_question_dict).execute()
        
        generated_questions.append(complete_generated_question)

    return generated_questions # return type: list of an instance of completeGeneratedQuestions.

def generate_problem_set(    
    data: GenerateProblemSetRequest,
    supabase: Client,
    access_token: str,
    refresh_token: str,
) -> CompleteProblemSet:
    problem_count = data.question_count
    category = data.category

    supabase.auth.set_session(access_token, refresh_token)
    user_id = supabase.auth.get_user().user.id

    problem_category_id_list = ProblemIdOfGivenCategories(category, None, supabase)

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
    complete_problem_set_dict['user_id'] = user_id
    data = supabase.table("exp_insertion_problem_set").insert(complete_problem_set_dict).execute()
    return complete_problem_set

def fetchSelectedQuestions(categorylv1, categorylv2, supabase):
    problem_category_id_list = ProblemIdOfGivenCategories(categorylv1, categorylv2, supabase)

    problems_ids = supabase.table("problems").select("id, question").execute()
    problems_ids_data = problems_ids.data
    questions = []

    for category_id in problems_ids_data:
        for category_id_l in problem_category_id_list:
            if category_id['id'] == category_id_l:
                if category_id not in questions:
                    questions.append(category_id)

    return questions

def ProblemIdOfGivenCategories(categorylv1, categorylv2, supabase):
    """
    To retrieve the corresponded id to the given category, 
    1. Retrived level 1 categories 
    2. Retrived level 2 categories only if there's no specified to the depth.
    3. Matched category ids with the ones in the prob_cat_cat 
    so that it takes a list of their problem ids to return.

    """
    problem_problem_categories_ids = supabase.table("problem_problem_categories").select("problem_id, category_id").execute()
    problem_categories = supabase.table("problem_categories").select("id, level1, level2").execute()
    problem_problem_categories_ids_data = problem_problem_categories_ids.data
    problem_categories_data = problem_categories.data
    problem_categories_list = []
    problem_categories_id_list = []
    res_list = []

    for retrived_category in problem_categories_data:
        if retrived_category['level1'] == categorylv1:
            problem_categories_list.append(retrived_category)
    if categorylv2 is not None:
        for retrived_category in problem_categories_list:
            if retrived_category['level2'] != categorylv2:
                problem_categories_list.remove(retrived_category)
    for found_category in problem_categories_list:
            problem_categories_id_list.append(found_category['id'])

    for category_id in problem_problem_categories_ids_data:
        for category_id_l in problem_categories_id_list:
            if category_id['category_id'] == category_id_l:
                res_list.append(category_id['problem_id'])

    return res_list

def solve_sympy(question: str) -> SympySolvedQuestion:
    sympy_translation = translate_to_sympy(question)
    output = execute_expression(sympy_translation.sympyression)
    sympy_solved_question = make_explanation_by_sympy_expression(
        question=question,
        sympy_expression=sympy_translation.sympy_expression,
        output=output,
    )
    return sympy_solved_question