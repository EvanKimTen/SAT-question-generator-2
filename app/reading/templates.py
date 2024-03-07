from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.prompts.prompt import PromptTemplate
from app.reading.parsers import generated_question_parser, preprocessed_passage_parser
from app.reading.prompts import (
    fix_json_parsing,
    function_category_preprocess,
    generic,
)
from app.db import supabase

def get_template(category_id):
    category = supabase.from_("problem_categories").select("generate_prompt").eq("id", category_id).execute()
    generate_prompt = category.data[0]["generate_prompt"]

    if generate_prompt is None:
        generate_prompt = generic.generate_prompt

    return ChatPromptTemplate(
        messages=[HumanMessagePromptTemplate.from_template(generate_prompt)],
        input_variables=[
            "example_question",
            "question_type",
            "selected_passage",
            "source_title",
        ],
        partial_variables={
            "format_instructions": generated_question_parser.get_format_instructions()
        },
    )


json_format_fix_prompt = PromptTemplate.from_template(
    fix_json_parsing.JSON_FORMAT_FIX_PROMPT
)

function_category_preprocess_prompt = PromptTemplate.from_template(
    function_category_preprocess.FUNCTION_CATEGORY_PREPROCESS_PROMPT,
    partial_variables={
        "format_instructions": preprocessed_passage_parser.get_format_instructions()
    },
)
