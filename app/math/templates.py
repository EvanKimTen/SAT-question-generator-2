from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from app.math.prompts import (
    math_generate_prompt,
    math_solve_prompt,
    sympy_translation_prompt,
    sympy_solved_question_prompt,
)
from app.math.parsers import (
    generated_question_parser,
    solution_with_choices_parser,
    sympy_translation_parser,
    sympy_solved_question_parser,
)


generate_question_template = ChatPromptTemplate(
    messages=[HumanMessagePromptTemplate.from_template(math_generate_prompt)],
    input_variables=[
        "major_category",
        "example_question",
        "question_type",
    ],
    partial_variables={
        "format_instructions": generated_question_parser.get_format_instructions()
    },
)


solve_question_template = ChatPromptTemplate(
    messages=[HumanMessagePromptTemplate.from_template(math_solve_prompt)],
    input_variables=["example_question", "question_type"],
    partial_variables={
        "format_instructions": solution_with_choices_parser.get_format_instructions()
    },
)


sympy_translation_template = ChatPromptTemplate(
    messages=[HumanMessagePromptTemplate.from_template(sympy_translation_prompt)],
    input_variables=["question"],
    partial_variables={
        "format_instructions": sympy_translation_parser.get_format_instructions()
    },
)

sympy_finalize_template = ChatPromptTemplate(
    messages=[HumanMessagePromptTemplate.from_template(sympy_solved_question_prompt)],
    input_variables=["question", "sympy_expression", "output"],
    partial_variables={
        "format_instructions": sympy_solved_question_parser.get_format_instructions()
    },
)
