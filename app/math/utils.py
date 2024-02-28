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


def inference_with_chatcompletion_model(prompt: str, model_name: str):
    chat = ChatOpenAI(model_name=model_name, openai_api_key=OPENAI_API_KEY)
    messages = [HumanMessage(content=prompt)]
    return chat(messages)


def generate_sat_question(
    major_one_category: MajorCategory,
    major_two_category: MajorCategory,
    major_three_category: MajorCategory,
    example_question: str,
    question_type: QuestionType,
):
    _input = generate_question_template.format_prompt(
        major_one_category=major_one_category,
        major_two_category=major_two_category,
        major_three_category=major_three_category,
        example_question=example_question,
        question_type=question_type,
    )
    output = chat_model(_input.to_messages())
    res = generated_question_parser.parse(output.content)
    return res


def solve_question(example_question: str, question_type: QuestionType):
    _input = solve_question_template.format_prompt(
        example_question=example_question, question_type=question_type
    )
    print(_input)
    output = chat_model(_input.to_messages())
    print(output) # In some cases, chat_model can't generate choices through the chat model.
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
