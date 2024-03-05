from supabase import Client
from app.math.utils import (
    generate_sat_question,
    solve_question,
    fetch_problems_by_category_ids,
    get_problem_ids_by_category_ids,
    generate_category_string
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
        category_questions = await fetch_problems_by_category_ids(data.category_ids, supabase)
        if not category_questions:
            example_question = "No example question found"
        else:
            example_question = random.choice(category_questions)
        
        categories_string = await generate_category_string(data.category_ids, supabase)
        generated_question = generate_sat_question(
            categories=categories_string,
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

    problem_category_id_list = await get_problem_ids_by_category_ids(category_ids, supabase)

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
        set=list_prob_set 
    )
    complete_problem_set_dict = complete_problem_set.dict()
    complete_problem_set_dict['user_id'] = user_id
    data = supabase.table("exp_insertion_problem_set").insert(complete_problem_set_dict).execute()
    return complete_problem_set
