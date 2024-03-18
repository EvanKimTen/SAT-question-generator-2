from app.reading.utils import generate_sat_question
from supabase import Client
from app.reading.schemas import (
    GenerateSimilarQuestionRequest,
    GenerateProblemSetRequest,
    CompleteGeneratedQuestion,
    CompleteProblemSet,
    QuestionInsideSet,
)

from app.core.utils import (
    fetch_problems_by_category_ids,
    get_problem_ids_by_category_ids,
)
from typing import List
import random

async def generate_problems(
    data: GenerateSimilarQuestionRequest,
    supabase: Client,
    access_token: str,
    refresh_token: str,
) -> List[CompleteGeneratedQuestion]:
    supabase.auth.set_session(access_token, refresh_token)
    user_id = supabase.auth.get_user().user.id

    question_count = data.question_count
    generated_questions = []
    category_questions = await fetch_problems_by_category_ids(
        [data.category_id]
    )
    display_id = ""
    display_id = display_id + "A" + str(1) # 1st digit
    list_diff = ["M1", "M2E", "M2H"]
    assigned_random_diff = random.choice(list_diff) 
    # There seemed to be no criteria for determining that difficulty --> takes the randomly chosen one
    if assigned_random_diff == "M1":
        display_id = display_id + str(1)
    elif assigned_random_diff == "M2E":
        display_id = display_id + str(2)
    elif assigned_random_diff == "M2H":
        display_id = display_id + str(3)
    # Assuming that I've added additional cols named module and subject to the probs table.
    # --> will address it later on the next push probably.
    problems_subject_and_module = (
        supabase.table("problems").select("*").match({'subject': "ENGLISH",'module': assigned_random_diff}).execute()
        ).data
    last_digit_field = len(problems_subject_and_module)
    if last_digit_field < 10:
        display_id = display_id + f"000{last_digit_field}"
    elif last_digit_field < 100:
        display_id = display_id + f"00{last_digit_field}"
    elif last_digit_field < 1000:
        display_id = display_id + f"0{last_digit_field}"
    elif last_digit_field < 10000:
        display_id = display_id + f"{last_digit_field}"
    for _ in range(question_count):
        generated_question = await generate_sat_question(
            category_id=data.category_id,
            example_question=category_questions,
            user_id=user_id,
            display_id=display_id
            # got an error here for empty seq --> need to generate more.
        )

        generated_questions.append(generated_question)

    return generated_questions


async def generate_problem_set(
    data: GenerateProblemSetRequest,
    supabase: Client,
    access_token: str,
    refresh_token: str,
) -> CompleteProblemSet:
    supabase.auth.set_session(access_token, refresh_token)
    user_id = supabase.auth.get_user().user.id

    problem_count = data.question_count
    problem_category_id_list = await get_problem_ids_by_category_ids(
        [data.category_id]
    )

    problems_ids = (
        supabase.table("problems").select("id, question, explanation").execute()
    )
    problem_set = []
    count = 0
    problems_ids_data = problems_ids.data

    for category_id in problems_ids_data:
        for category_id_l in problem_category_id_list:
            if problem_count == count:
                break
            if category_id["id"] == category_id_l:
                if category_id not in problem_set:
                    problem_set.append(category_id)
                    count += 1
    list_prob_set = []
    for problem in problem_set:
        complete_generated_question = QuestionInsideSet.parse_obj(problem)
        list_prob_set.append(complete_generated_question)

    # if the length of probelm_set is less than problem_count, raise an error.
    if len(list_prob_set) < problem_count:
        raise ValueError("Not enough problems to generate a problem set.")

    generated_test = (
        supabase.table("tests")
        .insert({"name": "New Problem Set", "is_full_test": False, "user_id": user_id})
        .execute()
    )
    generated_test_id = generated_test.data[0]["id"]

    # making complete problem set.
    complete_problem_set = CompleteProblemSet(
        id=generated_test_id,
        name="New Problem Set",
        is_full_test=False,
    )

    insert_data = []
    for problem in list_prob_set:
        insert_data.append(
            {
                "test_id": generated_test_id,
                "problem_id": problem.id,
                "subject": "ENGLISH",
            }
        )

    supabase.table("test_problems").insert(insert_data).execute()

    return complete_problem_set
