from supabase import Client
from app.test_gen.schema import Test, CompleteTestProblem, CompleteTestProblemSet
from app.core.utils import fetch_problems_by_category_ids
from app.test_gen.distribution_preset import (
    math_category_distribution,
    english_category_distribution,
)
import random


async def generate_test(
    supabase: Client,
    access_token: str,
    refresh_token: str,
) -> CompleteTestProblemSet:
    """
    1. Once getting the sum of the ratios in the preset,
    2. In a ratio to each category, you get multiple problems over iteration of math_category_distribution.
    """

    test_set = []
    total_questions = 154
    math_total_questions = 58
    eng_total_questions = 96
    whole_math_questions_list = []
    whole_eng_questions_list = []

    sum_ratios = 0
    for ratio in math_category_distribution.values():
        sum_ratios += ratio
    for category, ratio in math_category_distribution.items():
        ratio = ratio // sum_ratios
        num_questions_to_select = round(math_total_questions * ratio)
        category_questions = await fetch_problems_by_category_ids(category, supabase)
        # randomly_selected_questions = test_set.extend(random.sample(category_questions, num_questions_to_select))
        # for randomly_selected_question in randomly_selected_questions:
        #     complete_problems = CompleteTestProblem(
        #         test_id= 1, # be varied
        #         problem_id= randomly_selected_question['id'],
        #         module= None,
        #         test_subject= "MATH",
        #     ).dict()
        #     data = supabase.table("test_problems").insert(complete_problems).execute()
        whole_math_questions_list = whole_math_questions_list + list(category_questions)
    print(whole_math_questions_list)
    if len(test_set) < math_total_questions:  # In case the rounded one is not exact.
        addtional_list = []
        number_generate_more = math_total_questions - len(test_set)
        for i in range(number_generate_more):
            random_chosen_add_prob = random.choice(whole_math_questions_list)
            complete_problems = CompleteTestProblem(
                test_id=1,  # be varied
                problem_id=random_chosen_add_prob["id"],
                module="1",
                subject="MATH",
            ).dict()
            data = supabase.table("test_problems").insert(complete_problems).execute()
            addtional_list.append(random_chosen_add_prob)
        test_set = test_set + addtional_list

    # generating eng probs in the test again.

    sum_ratios = 0
    for ratio in english_category_distribution.values():
        sum_ratios += ratio
    for category, ratio in english_category_distribution.items():
        ratio = (ratio / sum_ratios) * 100
        num_questions_to_select = round(eng_total_questions * ratio)
        category_questions = fetch_problems_by_category_ids(category, supabase)
        # randomly_selected_questions = test_set.extend(random.sample(category_questions, num_questions_to_select))
        # for randomly_selected_question in randomly_selected_questions:
        #     complete_problems = CompleteTestProblem(
        #         test_id= 1, # be varied
        #         problem_id= randomly_selected_question['id'],
        #         module= None,
        #         test_subject= "ENGLISH",
        #     ).dict()
        #     data = supabase.table("test_problems").insert(complete_problems).execute()
        whole_eng_questions_list = whole_eng_questions_list + list(category_questions)
    if len(test_set) < total_questions:
        addtional_list = []
        number_generate_more = total_questions - len(test_set)
        for i in range(number_generate_more):
            random_chosen_add_prob = random.choice(whole_eng_questions_list)
            complete_problems = CompleteTestProblem(
                test_id=1,  # be varied
                problem_id=random_chosen_add_prob["id"],
                module="1",
                subject="ENGLISH",
            ).dict()
            data = supabase.table("test_problems").insert(complete_problems).execute()
            addtional_list.append(random_chosen_add_prob)
        test_set = test_set + addtional_list
    # TODO: insert the test_set into the database.

    supabase.auth.set_session(access_token, refresh_token)
    user_id = supabase.auth.get_user().user.id

    complete_test_set = Test(name="New Test", is_full_test=True, user_id=user_id).dict()
    data = supabase.table("tests").insert(complete_test_set).execute()
    # additional for checking the size of the dict.
    complete_test_prob_set = CompleteTestProblemSet(set=test_set)
    complete_test_prob_set_dict = complete_test_prob_set.dict()
    data = supabase.table("exp_test").insert(complete_test_prob_set_dict).execute()
    return complete_test_prob_set
