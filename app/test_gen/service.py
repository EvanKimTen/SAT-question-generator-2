from supabase import Client
from app.test_gen.schema import (
    CompleteTestSet
)
from app.writing.service import ProblemIdOfGivenCategories, fetchSelectedQuestions
from app.test_gen.distribution_preset import math_category_distribution, english_category_distribution
import random

def generate_test(
    supabase: Client,
    access_token: str,
    refresh_token: str,
    # current_user: UserData
) -> CompleteTestSet:
    """
    1. Once getting the sum of the ratios in the preset,
    2. In a ratio to each category, you get multiple problems over iteration of math_category_distribution.
    """
    
    supabase.auth.set_session(access_token, refresh_token)
    user_id = supabase.auth.get_user().user.id

    test_set = []
    math_total_questions = 58
    eng_total_questions = 96
    whole_math_questions_list = []
    whole_eng_questions_list = []
    subject = "math"
    sum_ratios = 0
    for ratio in math_category_distribution.values():
        sum_ratios += ratio
    for category, ratio in math_category_distribution.items():
        ratio = (ratio / sum_ratios) * 100
        num_questions_to_select = round(math_total_questions * ratio)
        category_questions = fetchSelectedQuestions(subject, category, supabase)
        test_set.extend(random.sample(category_questions, num_questions_to_select))
        whole_math_questions_list = whole_math_questions_list + list(category_questions.items())

    if len(test_set) < math_total_questions:
        addtional_list = []
        number_generate_more = math_total_questions - len(test_set)
        for i in range(number_generate_more):
            addtional_list.append(random.choice(whole_math_questions_list))
        test_set = test_set + addtional_list
    elif len(test_set) > math_total_questions:
        test_set = test_set[:153]

    # generating eng probs in the test again.
    subject = "english"
    sum_ratios = 0
    for ratio in english_category_distribution.values():
        sum_ratios += ratio
    for category, ratio in english_category_distribution.items():
        ratio = (ratio / sum_ratios) * 100
        num_questions_to_select = round(eng_total_questions * ratio)
        category_questions = fetchSelectedQuestions(subject, category, supabase)
        test_set.extend(random.sample(category_questions, num_questions_to_select))
        whole_eng_questions_list = whole_eng_questions_list + list(category_questions.items())

    if len(test_set) < eng_total_questions:
        addtional_list = []
        number_generate_more = eng_total_questions - len(test_set)
        for i in range(number_generate_more):
            addtional_list.append(random.choice(whole_eng_questions_list))
        test_set = test_set + addtional_list
    elif len(test_set) > eng_total_questions:
        test_set = test_set[:153]

    #TODO: insert the test_set into the database.
    
    # test_set["user_id"] = current_user.id
    # CompleteTestSet.parse_obj(test_set)
    return None

def ProblemIdOfGivenCategories(subject, category, supabase):
    problem_problem_categories_ids = supabase.table("problem_problem_categories").select("problem_id, category_id").execute()
    if subject == "math":
        problem_categories = supabase.table("problem_categories").select("id, level2").execute()
    elif subject == "english":
        problem_categories = supabase.table("problem_categories").select("id, level1").execute()
    problem_problem_categories_ids_data = problem_problem_categories_ids.data
    problem_categories_data = problem_categories.data
    problem_category_id_list = []
    category_id_list = []

    for retrived_category in problem_categories_data:
        if subject == "math":
            if retrived_category['level2'] == category:
                category_id_list.append(retrived_category['id'])
        elif subject == "english":
            if retrived_category['level1'] == category:
                category_id_list.append(retrived_category['id'])
            


    for category_id in problem_problem_categories_ids_data:
        for category_id_l in category_id_list:
            if category_id['category_id'] == category_id_l:
                problem_category_id_list.append(category_id['problem_id'])

    return problem_category_id_list


def fetchSelectedQuestions(subject, category, supabase):
    problem_category_id_list = ProblemIdOfGivenCategories(category, supabase)

    problems_ids = supabase.table("problems").select("id, question").execute()
    problems_ids_data = problems_ids.data
    questions = []

    for problem in problems_ids_data:
        for category_id_l in problem_category_id_list:
            if problem['id'] == category_id_l:
                if problem not in questions:
                    questions.append(problem)

    return questions