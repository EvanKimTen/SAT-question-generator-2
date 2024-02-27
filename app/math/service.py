from supabase import Client
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
    GenerateProblemSetRequest,
    GenerateTestSetRequest,
    CompleteGeneratedQuestion,
    CompleteProblemSet,
    CompleteTestSet,
    MajorCategory,
    QuestionType,
    ModelVersion,
    SympySolvedQuestion,
    subcategory_data,
)
from typing import List
import random
import json

def generate_problems(
    data: GenerateSimilarQuestionRequest,
    supabase_exp: Client
) -> List[CompleteGeneratedQuestion]:
    question_count = data.question_count
    generated_questions = []
    category_questions = fetchSelectedQuestions(data.major_one_category, supabase_exp)
    for _ in range(question_count):
        generated_question = generate_sat_question(
            major_one_category=data.major_one_category,
            major_two_category=data.major_two_category,
            sub_one_category=data.sub_one_category,
            sub_two_category=data.sub_two_category,
            example_question=random.choice(category_questions),
            question_type=data.question_type,
        )
        
        solution_with_choices = solve_question(
            example_question=generated_question.question,
            question_type=data.question_type,
        )
        print(solution_with_choices)
        complete_generated_question_data = {
            **generated_question.dict(),
            **solution_with_choices.dict(),
        }
        complete_generated_question = CompleteGeneratedQuestion.parse_obj(
            complete_generated_question_data
        )

        # Convert the Pydantic model to a dictionary
        complete_generated_question_dict = complete_generated_question.dict()

        # Serialize the dictionary to a JSON string
        complete_generated_question_json = json.dumps(complete_generated_question_dict)
        data = supabase_exp.table("problems").insert(complete_generated_question_json).execute()
        # if complete_generated_question.error:
        #     raise HTTPException(status_code=400, detail=generated_question.error.message)
        generated_questions.append(complete_generated_question)

    return generated_questions # return type: list of an instance of completeGeneratedQuestions.

def generate_problem_set(    
    data: GenerateProblemSetRequest,
    supabase_exp: Client
) -> List[CompleteProblemSet]:
    problem_count = data.question_count
    category = data.category

    problem_category_id_list = ProblemIdOfGivenCategories(category, supabase_exp)

    problems_ids = supabase_exp.table("problems").select("id, question, explanation").execute()
    problem_set = []
    problem_count = 2
    count = 0
    for problems_id in problems_ids:
        if problems_id is None:
            break
        prob_ids = problems_id[1]
        if prob_ids is not None:
            for category_id in prob_ids:
                for category_id_l in problem_category_id_list:
                    if problem_count == count:
                        break
                    if category_id['id'] == category_id_l:
                        if category_id not in problem_set:
                            problem_set.append(category_id)
                            count += 1
                            
    return problem_set

def generate_test(    
    data: GenerateTestSetRequest,
    supabase_exp: Client
) -> List[CompleteTestSet]:

    test_set = []
    total_questions = data.question_count
    modules = supabase_exp.table("test_problems").select("module").execute() 
    # More details needed for getting different module individually.
    for extractor in modules:
        if extractor is None:
            break
        for module in modules:
            if module == "1":
                category_distribution = {
                    "Linear Equations" : 0.07,
                    "Linear Function" : 0.07,
                    "System of Equations" : 0.07,
                    "Solving Inequalities" : 0.07,
                    "Graphing Inequalities" : 0.07,
                    "Absolute Value" : 0.038,
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
                sum_prob = 0
                for ratio in category_distribution.values():
                    sum_prob += ratio
                
                for category, ratio in category_distribution.items():
                    ratio = (ratio / sum_prob) * 100
                    num_questions_to_select = round(total_questions * ratio)
                    category_questions = fetchSelectedQuestions(category, supabase_exp)
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
    questions = []
    for problems_id in problems_ids:
        if problems_id is None:
            break
        prob_ids = problems_id[1]
        if prob_ids is not None:
            for category_id in prob_ids:
                for category_id_l in problem_category_id_list:
                    if category_id['id'] == category_id_l:
                        if category_id not in questions:
                            questions.append(category_id)
    
    return questions

def ProblemIdOfGivenCategories(category, supabase_exp):
    
    problem_problem_categories_ids = supabase_exp.table("problem_problem_categories").select("problem_id, category_id").execute()
    problem_category_id_list = []
    problem_categories = supabase_exp.table("problem_categories").select("id, level1").execute()
    category_id_list = []
    for problem_category in problem_categories:
        if problem_category is None:
            break
        categories = problem_category[1]
        if categories is not None:
            for retrived_category in categories:
                if retrived_category['level1'] == category:
                    category_id_list.append(retrived_category['id'])

    for problem_problem_categories_id in problem_problem_categories_ids:
        if problem_problem_categories_id is None:
            break
        category_ids = problem_problem_categories_id[1]
        if category_ids is not None:
            for category_id in category_ids:
                for category_id_l in category_id_list:
                    if category_id['category_id'] == category_id_l:
                        problem_category_id_list.append(category_id['problem_id'])

    return problem_category_id_list

def solve_sympy(question: str) -> SympySolvedQuestion:
    sympy_translation = translate_to_sympy(question)
    output = execute_expression(sympy_translation.sympy_expression)
    sympy_solved_question = make_explanation_by_sympy_expression(
        question=question,
        sympy_expression=sympy_translation.sympy_expression,
        output=output,
    )
    return sympy_solved_question