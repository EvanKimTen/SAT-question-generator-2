from app.reading.utils import generate_sat_question
from supabase import Client
from app.reading.schemas import (
    GenerateSimilarQuestionRequest,
    GenerateProblemSetRequest,
    CompleteGeneratedQuestion,
    CompleteProblemSet,
    QuestionInsideSet,
)

from app.core.utils import fetch_problems_by_category_ids, get_problem_ids_by_category_ids, generate_category_string
from typing import List

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
    category_questions = await fetch_problems_by_category_ids([data.category_id], supabase)
    category_string = await generate_category_string([data.category_id], supabase)
    for _ in range(question_count):
        generated_question = generate_sat_question(
            category=category_string,
            example_question=category_questions,
            user_id=user_id
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
    problem_category_id_list = await get_problem_ids_by_category_ids([data.category_id], supabase)

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

    generated_test = supabase.table("tests").insert({"name": "New Problem Set", "is_full_test": False, "user_id": user_id}).execute()
    generated_test_id = generated_test.data[0]['id']
    
    # making complete problem set.
    complete_problem_set = CompleteProblemSet(
        id=generated_test_id,
        name="New Problem Set",
        is_full_test=False,
    )

    insert_data = []
    for problem in list_prob_set:
        insert_data.append({"test_id": generated_test_id, "problem_id": problem.id, "subject": "ENGLISH"})

    supabase.table("test_problems").insert(insert_data).execute()

    return complete_problem_set
