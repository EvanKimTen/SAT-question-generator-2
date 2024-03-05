from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
)
from app.math.templates import (
    generate_question_template,
    solve_question_template,
    sympy_translation_template,
    sympy_finalize_template,
)
from app.math.parsers import (
    generated_question_parser,
    solution_with_choices_parser,
    sympy_translation_parser,
    sympy_solved_question_parser,
)
from app.math.schemas import (
    QuestionType,
    MajorCategory,
    SympyTranslation,
    SympySolvedQuestion,
)
from app.constants import OPENAI_API_KEY
from sympy import *

# only below two models are supported for json response
# model_name = "gpt-3.5-turbo-0125"
model_name = "gpt-4-turbo-preview"
chat_model = ChatOpenAI(
    model_name=model_name, openai_api_key=OPENAI_API_KEY, max_tokens=1000, model_kwargs={"response_format":{ "type": "json_object" }},
)

async def generate_category_string(categories: list, supabase) -> list:
    category_strings = []
    for category in categories:
        query = supabase.from_("problem_categories").select("level1, level2, level3").eq("id", category)

        result = query.execute()

        concatenated_string = f"{result.data[0]['level1']} {result.data[0]['level2'] or ''} {result.data[0]['level3'] or ''}"
        print(concatenated_string)

        category_strings.append(concatenated_string)
    print(category_strings)
    return category_strings


async def fetch_problems_by_category_ids(category_ids: list, supabase):
    problem_category_id_list = await get_problem_ids_by_category_ids(category_ids, supabase)

    problems_ids = supabase.table("problems").select("id, question").execute()
    problems_ids_data = problems_ids.data
    questions = []

    for category_id in problems_ids_data:
        for category_id_l in problem_category_id_list:
            if category_id['id'] == category_id_l:
                if category_id not in questions:
                    questions.append(category_id)

    return questions


async def get_problem_ids_by_category_ids(category_ids: list, supabase) -> list:
    """
    To retrieve the corresponding id to the given category, 
    1. Retrieve level 1 categories 
    2. Retrieve level 2 categories only if there's no specified depth.
    3. Match category IDs with the ones in the prob_cat_cat 
    to return a list of their problem IDs.

    """
    problem_problem_categories = supabase.table("problem_problem_categories") \
                                            .select("problem_id, category_id") \
                                            .execute()

    #FIXME: ids will be string, temporarily change category_ids element to int
    category_ids = list(map(int, category_ids))

    data = problem_problem_categories.data
    problem_category_dict = {}
    for d in data:
        if d['problem_id'] in problem_category_dict:
            problem_category_dict[d['problem_id']].append(d['category_id'])
        else:
            problem_category_dict[d['problem_id']] = [d['category_id']]

    filtered_problem_ids = []
    for problem_id, category_list in problem_category_dict.items():
        if set(category_list) == set(category_ids):
            filtered_problem_ids.append(problem_id)
            
    return filtered_problem_ids


def solve_sympy(question: str) -> SympySolvedQuestion:
    sympy_translation = translate_to_sympy(question)
    output = execute_expression(sympy_translation.sympyression)
    sympy_solved_question = make_explanation_by_sympy_expression(
        question=question,
        sympy_expression=sympy_translation.sympy_expression,
        output=output,
    )
    return sympy_solved_question


def inference_with_chatcompletion_model(prompt: str, model_name: str):
    chat = ChatOpenAI(model_name=model_name, openai_api_key=OPENAI_API_KEY)
    messages = [HumanMessage(content=prompt)]
    return chat(messages)


def generate_sat_question(
    categories: list,
    example_question: str,
    question_type: QuestionType,
):
    _input = generate_question_template.format_prompt(
        category=categories,
        example_question=example_question,
        question_type=question_type,
    )
    print(_input)
    output = chat_model(_input.to_messages())
    res = generated_question_parser.parse(output.content)
    return res


def solve_question(example_question: str, question_type: QuestionType):
    _input = solve_question_template.format_prompt(
        example_question=example_question, question_type=question_type
    )
    print(_input)
    output = chat_model(_input.to_messages())
    res = solution_with_choices_parser.parse(output.content)
    return res


def translate_to_sympy(question: str) -> SympyTranslation:
    _input = sympy_translation_template.format_prompt(question=question)
    output = chat_model(_input.to_messages())
    return sympy_translation_parser.parse(output.content)


def execute_expression(sympy_expression):
    exec(sympy_expression, globals())
    return str(output)


def make_explanation_by_sympy_expression(
    question: str, sympy_expression: str, output: str
) -> SympySolvedQuestion:
    _input = sympy_finalize_template.format_prompt(
        question=question,
        sympy_expression=sympy_expression,
        output=output,
    )
    output = chat_model(_input.to_messages())
    solved_question = sympy_solved_question_parser.parse(output.content)

    sympy_solved_question = SympySolvedQuestion(
        correct_answer=solved_question.correct_answer,
        sympy_expression=sympy_expression,
        explanation=solved_question.explanation,
    )

    return sympy_solved_question
