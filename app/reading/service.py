from app.reading.utils import generate_sat_question
from supabase import Client
from app.reading.schemas import (
    GenerateSimilarQuestionRequest,
    GenerateProblemSetRequest,
    CompleteGeneratedQuestion,
    CompleteProblemSet,
    QuestionInsideSet,
    Category,
    QuestionType,
    ModelVersion,
)
from datetime import datetime, timedelta
from typing import List
import random
import json

def generate_problems(
    data: GenerateSimilarQuestionRequest,
    supabase: Client
) -> List[CompleteGeneratedQuestion]:
    question_count = data.question_count
    generated_questions = []
    category_questions = fetchSelectedQuestions(data.category, supabase)

    for _ in range(question_count):
        generated_question = generate_sat_question(
            category=data.category,
            example_question=category_questions,
            # got an error here for empty seq --> need to generate more.
        )
        generated_questions.append(generated_question)

    return generated_questions

def generate_problem_set(
    data: GenerateProblemSetRequest,
    supabase: Client
) -> CompleteProblemSet:
    problem_count = data.question_count
    category = data.category
    problem_category_id_list = ProblemsIdOfGivenCategories(category, supabase)

    problems_ids = supabase.table("problems").select("id, question, explanation").execute()
    problem_set = []
    count = 0
    problems_ids_data = problems_ids.data

    for category_id in problems_ids_data:
        for category_id_l in problem_category_id_list:
            if problem_count == count:
                break
            if category_id['id'] == category_id_l:
                if category_id not in problem_set:
                    problem_set.append(category_id)
                    count += 1
    list_prob_set = []
    for problem in problem_set:
        complete_generated_question = QuestionInsideSet.parse_obj(
            problem
        )
        list_prob_set.append(complete_generated_question)
    print(list_prob_set)
    # making complete problem set.
    
    complete_problem_set = CompleteProblemSet(
        name="New Problem Set",
        is_full_test=False,
        # user_id=12,
        set=list_prob_set 
    )
    complete_problem_set_dict = complete_problem_set.dict()
    data = supabase.table("exp_insertion_problem_set").insert(complete_problem_set_dict).execute()
    return complete_problem_set



def fetchSelectedQuestions(category, supabase):
    problem_category_id_list = ProblemsIdOfGivenCategories(category, supabase)

    problems_ids = supabase.table("problems").select("id, question").execute()
    problems_ids_data = problems_ids.data
    questions = []

    for category_id in problems_ids_data:
        for category_id_l in problem_category_id_list:
            if category_id['id'] == category_id_l:
                if category_id not in questions:
                    questions.append(category_id)
    
    return questions

def ProblemsIdOfGivenCategories(category, supabase):
    
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

# def get_category_list():
#     return list(Category)


# def get_question_type_list():
#     return list(QuestionType)


# def get_model_version_list():
#     return list(ModelVersion)
