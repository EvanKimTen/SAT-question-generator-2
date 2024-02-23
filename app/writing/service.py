from fastapi import HTTPException
from supabase import create_client, Client
from app.writing.schemas import (
    GenerateSimilarQuestionRequest,
    GenerateTestSetRequest,
    CompleteGeneratedQuestion,
    CompleteProblemSet,
    CompleteTestSet,
)

from app.writing.utils import generate_sat_question

from typing import List
import random
import json

def generate_questions(
    data: GenerateSimilarQuestionRequest,
    supabase_exp: Client
) -> List[CompleteGeneratedQuestion]:
# process parameter to send back in the form of CompleteGeneratedQuestion.
    question_count = data.question_count
    generated_questions = []

    for _ in range(question_count):
        generated_question = generate_sat_question(
            category=data.category,
            example_question=data.example_question,
        )
        complete_generated_question = CompleteGeneratedQuestion.parse_obj(
            generated_question
        )
        complete_generated_question_dict = complete_generated_question.dict()
        complete_generated_question_json = json.dumps(complete_generated_question_dict)
        supabase_exp.table("problems").insert(complete_generated_question_json).execute()
        # if generated_question.error:
        #     raise HTTPException(status_code=400, detail=generated_question.error.message)
        generated_questions.append(complete_generated_question)

    return generated_questions

def generate_problem_set(
    data: GenerateSimilarQuestionRequest,
    supabase_exp: Client
) -> List[CompleteProblemSet]:
    problem_count = data.question_count
    problem_set = []
    problems = supabase_exp.table("problems").select("question, explanation").execute()
    count = 0
    for extractor in problems:
        if extractor is None:
            break
        sep_problems = extractor[1]
        if sep_problems is not None:
            for problem in sep_problems:
                if problem_count == count: 
                    break
                problem_set.append(problem)
                count += 1
    return problem_set

def generate_test(
    data: GenerateTestSetRequest,
    supabase_exp: Client
) -> List[CompleteTestSet]:
    test_set = []
    total_questions = data.question_count

    extracted = supabase_exp.table("test_problems").select("module").execute() 
    # More details needed for getting different module individually.

    for extractor in extracted:
        if extractor is None:
            break
        modules = extractor[1]
        if modules is not None:
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
                        for category, ratio in category_distribution.items():
                            category_questions, num_questions_to_select = randomlySelectProblems(category, ratio, total_questions)
                            test_set.extend(random.sample(category_questions, num_questions_to_select))

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
                    for category, ratio in category_distribution.items():
                        category_questions, num_questions_to_select = randomlySelectProblems(category, ratio, total_questions)
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
                    for category, ratio in category_distribution.items():
                        category_questions, num_questions_to_select = randomlySelectProblems(category, ratio, total_questions)
                        test_set.extend(random.sample(category_questions, num_questions_to_select))
    return []

def randomlySelectProblems(category, ratio, total_questions, supabase_exp):
    num_questions_to_select = round(total_questions * ratio)
    query = f"""
    SELECT problems.question
    FROM problems
    INNER JOIN problem_problem_categories ON problem_problem_categories.category_id = problems.id
    INNER JOIN problem_categories ON problem_problem_categories.category_id = problem_categories.id
    WHERE problem_categories.level1 = '{category}'
    """
    category_questions = supabase_exp.table("problems").execute_sql(query)
    
    return num_questions_to_select, category_questions

    

                