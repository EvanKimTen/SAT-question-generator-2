from supabase import Client
from app.math.utils import (
    generate_sat_question,
    solve_question,
    fetch_problems_by_category_ids,
    get_problem_ids_by_category_ids,
    generate_category_string,
)
from app.math.schemas import (
    GenerateSimilarQuestionRequest,
    GenerateProblemSetRequest,
    CompleteGeneratedQuestion,
    CompleteProblemSet,
    GeneratedQuestion,
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

    generated_questions = []
    question_count = data.question_count
    question_type = data.question_type

    for _ in range(question_count):
        category_questions = await fetch_problems_by_category_ids(
            data.category_ids, supabase
        )
        if not category_questions:
            example_question = "No example question found"
        else:
            example_question = random.choice(category_questions)
        display_id = ""
        display_id = display_id + "A" + str(2) # 1st digit: Math
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
            supabase.table("problems").select("*").match({'subject': "MATH",'module': assigned_random_diff}).execute()
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
        categories_string = await generate_category_string(data.category_ids, supabase)
        generated_question = generate_sat_question(
            categories=categories_string,
            example_question=example_question,
            question_type=question_type,
            display_id = display_id
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
        passage_dict = {"passage": None}
        complete_generated_question_dict = (
            passage_dict | complete_generated_question_dict
        )
        complete_generated_question_dict["user_id"] = user_id
        complete_generated_question_dict["display_id"] = display_id
        generated_problem = (
            supabase.table("problems")
            .insert(complete_generated_question_dict)
            .execute()
        )
        generated_problem_id = generated_problem.data[0]["id"]
        for category_id in data.category_ids:
            supabase.table("problem_problem_categories").insert(
                {"problem_id": generated_problem_id, "category_id": category_id}
            ).execute()

        generated_questions.append(complete_generated_question)

    return generated_questions  # return type: list of an instance of completeGeneratedQuestions.


async def generate_problem_set(
    data: GenerateProblemSetRequest,
    supabase: Client,
    access_token: str,
    refresh_token: str,
) -> CompleteProblemSet:
    problem_count = data.question_count
    category_ids = data.category_ids
    supabase.auth.set_session(access_token, refresh_token)
    user_id = supabase.auth.get_user().user.id

    problem_category_id_list = await get_problem_ids_by_category_ids(
        category_ids, supabase
    )

    problems_ids = (
        supabase.table("problems").select("id, question, explanation").execute()
    )
    problems_ids_data = problems_ids.data
    problem_set = []
    problem_count = data.question_count
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
        complete_generated_question = GeneratedQuestion.parse_obj(problem)
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
            {"test_id": generated_test_id, "problem_id": problem.id, "subject": "MATH"}
        )

    supabase.table("test_problems").insert(insert_data).execute()
    return complete_problem_set
