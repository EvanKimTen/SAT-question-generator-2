from math.router import supabase
from fastapi import HTTPException
from app.math.utils import (
    generate_sat_question,
    solve_question,
    translate_to_sympy,
    make_explanation_by_sympy_expression,
    execute_expression,
)
from app.math.schemas import (
    GenerateSimilarQuestionRequest,
    CompleteGeneratedQuestion,
    MajorCategory,
    QuestionType,
    ModelVersion,
    SympySolvedQuestion,
    subcategory_data,
)
from typing import List
import random

def generate_questions(
    data: GenerateSimilarQuestionRequest,
) -> List[CompleteGeneratedQuestion]:
    question_count = data.question_count
    generated_questions = []

    for _ in range(question_count):
        generated_question = generate_sat_question(
            major_one_category=data.major_one_category,
            major_two_category=data.major_two_category,
            sub_one_category=data.sub_one_category,
            sub_two_category=data.sub_two_category,
            example_question=data.example_question,
            question_type=data.question_type,
        )
        solution_with_choices = solve_question(
            example_question=generated_question.question,
            question_type=data.question_type,
        )
        complete_generated_question_data = {
            **generated_question.dict(),
            **solution_with_choices.dict(),
        }
        complete_generated_question = CompleteGeneratedQuestion.parse_obj(
            complete_generated_question_data
        )
        supabase.table("problems").insert(complete_generated_question).execute()
        if complete_generated_question.error:
            raise HTTPException(status_code=400, detail=generated_question.error.message)
        generated_questions.append(complete_generated_question)

    return generated_questions

def generate_problem_set(    
    data: GenerateSimilarQuestionRequest,
) -> List[CompleteGeneratedQuestion]:
    question_count = data.question_count
    question_set = []
    for _ in range(question_count):
        question = supabase.table("problems").select("*").eq("question").execute() # will modify soon once
        # grasp a gist of the db contents.
        question_set.append(question)

    return question_set

def generate_test_set(    
    data: GenerateSimilarQuestionRequest,
) -> List[CompleteGeneratedQuestion]:

    test_set = []
    total_questions = data.question_count
    modules = supabase.table("test_problems").select("module").execute() 
    # More details needed for getting different module individually.

    for module in modules:
        if module == "1":
            category_distribution = {
                "Linear Equations" : 0.07,
                "Linear Function" : 0.07,
                "System of Equations" : 0.07,
                "Solving Inequalities" : 0.07,
                "Graphing Inequalities" : 0.07,
                "Absolute Value " : 0.038,
                "Exponential Equations" : 0.038,
                "Radical Equation and Function" : 0.038,
                "Complex Numbers" : 0.038,
                "Quadratic Equation" : 0.038,
                "Polynomial Equation" : 0.038,
                "Rational Equation" : 0.038,
                "Functions" : 0.038,
                "Transformation": 0.038,
                "Ratio, Rate, and Proportion" : 0.0375,
                "Percentage" : 0.0375,
                "Probability" :0.0375,
                "Statistics": 0.0375,
                "Angles, Triangles, and Polygons" : 0.0375,
                "Circle" : 0.0375,
                "Congruence and Similarity of Triangles" : 0.0375,
                "Polygon in plane / Circle Equation" : 0.0375,
                "Volume (feat. Surface Area)" : 0.0375,
                "Trigonometric Ratio" : 0.0375,
            }
            for category, ratio in category_distribution.items():
                category_questions, num_questions_to_select = randomlySelectProblems(category, ratio, total_questions)
                test_set.extend(random.sample(category_questions, num_questions_to_select))

        elif module == "2-easy":
            category_distribution = {
                "Linear Equations" : 0.07,
                "Linear Function" : 0.07,
                "System of Equations" : 0.07,
                "Solving Inequalities" : 0.07,
                "Graphing Inequalities" : 0.07,
                "Absolute Value " : 0.038,
                "Exponential Equations" : 0.038,
                "Radical Equation and Function" : 0.038,
                "Complex Numbers" : 0.038,
                "Quadratic Equation" : 0.038,
                "Polynomial Equation" : 0.038,
                "Rational Equation" : 0.038,
                "Functions" : 0.038,
                "Transformation": 0.038,
                "Ratio, Rate, and Proportion" : 0.0375,
                "Percentage" : 0.0375,
                "Probability" :0.0375,
                "Statistics": 0.0375,
                "Angles, Triangles, and Polygons" : 0.0375,
                "Circle" : 0.0375,
                "Congruence and Similarity of Triangles" : 0.0375,
                "Polygon in plane / Circle Equation" : 0.0375,
                "Volume (feat. Surface Area)" : 0.0375,
                "Trigonometric Ratio" : 0.0375,
            }
            for category, ratio in category_distribution.items():
                category_questions, num_questions_to_select = randomlySelectProblems(category, ratio, total_questions)
                test_set.extend(random.sample(category_questions, num_questions_to_select))

        elif module == "2-hard":
            category_distribution = {
                "Linear Equations" : 0.07,
                "Linear Function" : 0.07,
                "System of Equations" : 0.07,
                "Solving Inequalities" : 0.07,
                "Graphing Inequalities" : 0.07,
                "Absolute Value " : 0.038,
                "Exponential Equations" : 0.038,
                "Radical Equation and Function" : 0.038,
                "Complex Numbers" : 0.038,
                "Quadratic Equation" : 0.038,
                "Polynomial Equation" : 0.038,
                "Rational Equation" : 0.038,
                "Functions" : 0.038,
                "Transformation": 0.038,
                "Ratio, Rate, and Proportion" : 0.0375,
                "Percentage" : 0.0375,
                "Probability" :0.0375,
                "Statistics": 0.0375,
                "Angles, Triangles, and Polygons" : 0.0375,
                "Circle" : 0.0375,
                "Congruence and Similarity of Triangles" : 0.0375,
                "Polygon in plane / Circle Equation" : 0.0375,
                "Volume (feat. Surface Area)" : 0.0375,
                "Trigonometric Ratio" : 0.0375,
            }
            for category, ratio in category_distribution.items():
                category_questions, num_questions_to_select = randomlySelectProblems(category, ratio, total_questions)
                test_set.extend(random.sample(category_questions, num_questions_to_select))
    return test_set

def randomlySelectProblems(category, ratio, total_questions):
    num_questions_to_select = round(total_questions * ratio)
    query = f"""
    SELECT problems.question
    FROM problems
    INNER JOIN problem_problem_categories ON problem_problem_categories.category_id = problems.id
    INNER JOIN problem_categories ON problem_problem_categories.category_id = problem_categories.id
    WHERE problem_categories.level1 = '{category}'
    """
    category_questions = supabase.table("problems").execute_sql(query)
    return num_questions_to_select, category_questions

def solve_sympy(question: str) -> SympySolvedQuestion:
    sympy_translation = translate_to_sympy(question)
    output = execute_expression(sympy_translation.sympy_expression)
    sympy_solved_question = make_explanation_by_sympy_expression(
        question=question,
        sympy_expression=sympy_translation.sympy_expression,
        output=output,
    )
    return sympy_solved_question