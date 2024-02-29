from fastapi import HTTPException
from supabase import create_client, Client
from app.writing.schemas import (
    GenerateSimilarQuestionRequest,
    GenerateProblemSetRequest,
    GenerateTestSetRequest,
    CompleteGeneratedQuestion,
    CompleteProblemSet,
    CompleteTestSet,
    GeneratedQuestion,
)

from app.writing.utils import generate_sat_question

from datetime import datetime, timedelta
from typing import List
import random
import json

def generate_problems(
    data: GenerateSimilarQuestionRequest,
    supabase_exp: Client
) -> List[CompleteGeneratedQuestion]:
# process parameter to send back in the form of CompleteGeneratedQuestion.
    question_count = data.question_count
    generated_questions = []
    category_questions = fetchSelectedQuestions(data.category, supabase_exp)
    for _ in range(question_count):
        complete_generated_question = generate_sat_question(
            category=data.category,
            example_question=random.choice(category_questions),
        )

        print(type(complete_generated_question))
        created_at = datetime.utcnow() - timedelta(hours=2)
        creation_date = {}
        creation_date["id"] = 1
        creation_date["created_at"] = str(created_at)
        complete_generated_question_dict = complete_generated_question.dict()
        creation_date.update(complete_generated_question_dict)
        complete_generated_question_dict = creation_date
        print(complete_generated_question_dict)
        complete_generated_question_json = json.dumps(complete_generated_question_dict)
        print(complete_generated_question_json)

        data = supabase_exp.table("experiment_for_insertion").insert(complete_generated_question_json).execute()
        print(data)
        # if generated_question.error:
        #     raise HTTPException(status_code=400, detail=generated_question.error.message)
        generated_questions.append(complete_generated_question)

    return generated_questions

def generate_problem_set(
    data: GenerateProblemSetRequest,
    supabase_exp: Client
) -> List[CompleteProblemSet]:
    """

    """
    problem_count = data.question_count # 54
    
    category = data.category
    problem_category_id_list = ProblemIdOfGivenCategories(category, supabase_exp)

    problems_ids = supabase_exp.table("problems").select("id, question, explanation").execute()
    problems_ids_data = problems_ids.data
    problem_set = []
    count = 0
    
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
        complete_generated_question = GeneratedQuestion(
            problem
        )
        list_prob_set.append(complete_generated_question)

    # making complete problem set.
    created_at = datetime.utcnow() - timedelta(hours=2)
    creation_date = {"created_at": str(created_at)}
    
    complete_problem_set = CompleteProblemSet(
        name="New Problem Set",
        is_full_test=False,
        user_id=12,
        set=list_prob_set 
    )
    # complete_problem_set_dict = complete_problem_set.dict()
    # data = supabase_exp.table("problems").insert(complete_problem_set_dict).execute()
    print(type(complete_problem_set))
    return complete_problem_set

def generate_test(
    data: GenerateTestSetRequest,
    supabase_exp: Client
) -> List[CompleteTestSet]:
    test_set = []
    total_questions = data.question_count

    extracted_module = supabase_exp.table("test_problems").select("module").execute() 
    # More details needed for getting different module individually.
    modules = extracted_module.data
    
    for module in modules:
        if module['module'] == '1':
                category_distribution = {
                    "Craft & Structure" : 0.28,
                    "Accomplishing the Goal": 0.26,
                    "Subject-verb Agreement": 0.0325,
                    "Pronoun-Antecedent Agreement": 0.0325,
                    "Verb forms - Tense": 0.0325,
                    "Verb forms - Finite vs. Non-finite": 0.0325,
                    "Subject-Modifier Placement": 0.0325,
                    "Plural and possessive nouns": 0.0325,
                    "Linking clauses": 0.0325,
                    "Supplements": 0.0325,
                    "Punctuations": 0.0325,        
                    "Transitions": 0.20
                }
                sum_prob = 0
                for ratio in category_distribution.values():
                    sum_prob += ratio
                for category, ratio in category_distribution.items():
                    ratio = (ratio / sum_prob) * 100
                    num_questions_to_select = round(total_questions * ratio)
                    category_questions = fetchSelectedQuestions(category, supabase_exp)
                    test_set.extend(random.sample(category_questions, num_questions_to_select))
                    # should generate more problems then gonna be resolved.

        elif module == "2-easy":
            category_distribution = {
                "Craft & Structure" : 0.28, #
                "Accomplishing the Goal": 0.26,
                "Subject-verb Agreement": 0.0325,
                "Pronoun-Antecedent Agreement": 0.0325,
                "Verb forms - Tense": 0.0325,
                "Verb forms - Finite vs. Non-finite": 0.0325,
                "Subject-Modifier Placement": 0.0325,
                "Plural and possessive nouns": 0.0325,
                "Linking clauses": 0.0325,
                "Supplements": 0.0325,
                "Punctuations": 0.0325,        
                "Transitions": 0.20
            }
            sum_prob = 0
            for ratio in category_distribution.values():
                sum_prob += ratio
            for category, ratio in category_distribution.items():
                ratio = (ratio / sum_prob) * 100
                num_questions_to_select = round(total_questions * ratio)
                category_questions = fetchSelectedQuestions(category, supabase_exp)
                test_set.extend(random.sample(category_questions, num_questions_to_select))

        elif module == "2-hard":
            category_distribution = {
                "Craft & Structure" : 0.28, #
                "Accomplishing the Goal": 0.26,
                "Subject-verb Agreement": 0.0325,
                "Pronoun-Antecedent Agreement": 0.0325,
                "Verb forms - Tense": 0.0325,
                "Verb forms - Finite vs. Non-finite": 0.0325,
                "Subject-Modifier Placement": 0.0325,
                "Plural and possessive nouns": 0.0325,
                "Linking clauses": 0.0325,
                "Supplements": 0.0325,
                "Punctuations": 0.0325,        
                "Transitions": 0.20
            }
            sum_prob = 0
            for ratio in category_distribution.values():
                sum_prob += ratio
            for category, ratio in category_distribution.items():
                ratio = (ratio / sum_prob) * 100
                num_questions_to_select = round(total_questions * ratio)
                category_questions = fetchSelectedQuestions(category, supabase_exp)
                test_set.extend(random.sample(category_questions, num_questions_to_select))
    return test_set

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


                