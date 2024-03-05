from fastapi import HTTPException
from supabase import Client
from app.writing.schemas import (
    GenerateSimilarQuestionRequest,
    GenerateProblemSetRequest,
    CompleteGeneratedQuestion,
    CompleteProblemSet,
    GeneratedQuestion,
)
from app.core.utils import (
    fetch_problems_by_category_ids,
    get_problem_ids_by_category_ids,
)
from app.writing.utils import generate_sat_question
from typing import List
import random


async def generate_problems(
    data: GenerateSimilarQuestionRequest,
    supabase: Client,
    access_token: str,
    refresh_token: str,
) -> List[CompleteGeneratedQuestion]:
    # process parameter to send back in the form of CompleteGeneratedQuestion.
    question_count = data.question_count
    generated_questions = []
    supabase.auth.set_session(access_token, refresh_token)
    user_id = supabase.auth.get_user().user.id
    category_questions = await fetch_problems_by_category_ids(
        [data.category_id], supabase
    )
    if not category_questions:
        example_question = "No example question found"
    else:
        example_question = random.choice(category_questions)

    for _ in range(question_count):
        complete_generated_question = generate_sat_question(
            category="Punctuations",  # FIXME: category should be passed from the request.
            example_question=example_question,
        )
        complete_generated_question_dict = complete_generated_question.dict()
        complete_generated_question_dict["user_id"] = user_id
        generated_problem = (
            supabase.table("problems")
            .insert(complete_generated_question_dict)
            .execute()
        )
        # get the id of the generated question and insert it into the problem_problem_categories table.
        generated_problem_id = generated_problem.data[0]["id"]
        supabase.table("problem_problem_categories").insert(
            {"problem_id": generated_problem_id, "category_id": data.category_id}
        ).execute()
        generated_questions.append(complete_generated_question_dict)

    return generated_questions


async def generate_problem_set(
    data: GenerateProblemSetRequest,
    supabase: Client,
    access_token: str,
    refresh_token: str,
) -> CompleteProblemSet:
    supabase.auth.set_session(access_token, refresh_token)
    user_id = supabase.auth.get_user().user.id

    problem_count = data.question_count  # 54
    problem_category_id_list = await get_problem_ids_by_category_ids(
        [data.category_id], supabase
    )
    problems_ids = (
        supabase.table("problems").select("id, question, explanation").execute()
    )
    problems_ids_data = problems_ids.data
    problem_set = []
    count = 0
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
        complete_generated_question = GeneratedQuestion.parse_obj(problem)
        list_prob_set.append(complete_generated_question)

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
