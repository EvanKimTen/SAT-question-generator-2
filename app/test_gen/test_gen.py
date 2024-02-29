from supabase import Client
from app.writing.schemas import (
    GenerateTestSetRequest,
    CompleteTestSet,
)
import random
from app.test_gen.distribution_preset import math_category_distribution, english_category_distribution

def generate_test(
    supabase_exp: Client
) -> CompleteTestSet:
    test_set = []
    total_questions = 140

    extracted_module = supabase_exp.table("test_problems").select("module, subject").execute() 
    # More details needed for getting different module individually.
    modules = extracted_module.data

    for module in modules:
        if module == "1":
            sum_prob = 0
            for ratio in math_category_distribution.values():
                sum_prob += ratio
            
            for category, ratio in math_category_distribution.items():
                ratio = (ratio / sum_prob) * 100
                num_questions_to_select = round(total_questions * ratio)
                category_questions = fetchSelectedQuestions(category, supabase_exp)
                test_set.extend(random.sample(category_questions, num_questions_to_select))

        elif module == "2-easy":
            sum_prob = 0
            for ratio in math_category_distribution.values():
                sum_prob += ratio
            
            for category, ratio in math_category_distribution.items():
                ratio = (ratio / sum_prob) * 100
                num_questions_to_select = round(total_questions * ratio)
                category_questions = fetchSelectedQuestions(category, supabase_exp)
                test_set.extend(random.sample(category_questions, num_questions_to_select))

        elif module == "2-hard":
            sum_prob = 0
            for ratio in math_category_distribution.values():
                sum_prob += ratio
            
            for category, ratio in math_category_distribution.items():
                ratio = (ratio / sum_prob) * 100
                num_questions_to_select = round(total_questions * ratio)
                category_questions = fetchSelectedQuestions(category, supabase_exp)
                test_set.extend(random.sample(category_questions, num_questions_to_select))

    for module in modules:
        if module == "1":
            sum_prob = 0
            for ratio in english_category_distribution.values():
                sum_prob += ratio
            for category, ratio in english_category_distribution.items():
                ratio = (ratio / sum_prob) * 100
                num_questions_to_select = round(total_questions * ratio)
                category_questions = fetchSelectedQuestions(category, supabase_exp)
                test_set.extend(random.sample(category_questions, num_questions_to_select))
                # generating more problems then gonna be resolved.

        elif module == "2-easy":
            sum_prob = 0
            for ratio in english_category_distribution.values():
                sum_prob += ratio
            for category, ratio in english_category_distribution.items():
                ratio = (ratio / sum_prob) * 100
                num_questions_to_select = round(total_questions * ratio)
                category_questions = fetchSelectedQuestions(category, supabase_exp)
                test_set.extend(random.sample(category_questions, num_questions_to_select))

        elif module == "2-hard":
            sum_prob = 0
            for ratio in english_category_distribution.values():
                sum_prob += ratio
            for category, ratio in english_category_distribution.items():
                ratio = (ratio / sum_prob) * 100
                num_questions_to_select = round(total_questions * ratio)
                category_questions = fetchSelectedQuestions(category, supabase_exp)
                test_set.extend(random.sample(category_questions, num_questions_to_select))
    return test_set

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