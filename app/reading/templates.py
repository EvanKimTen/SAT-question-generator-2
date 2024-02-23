from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.prompts.prompt import PromptTemplate
from app.reading.parsers import generated_question_parser
from app.reading.schemas import Category
from app.reading.prompts import (
    function_lit,
    function_sci_ss,
    purpose_lit,
    purpose_sci_ss,
    fix_json_parsing,
    function_category_preprocess,
)

PROMPTS = {
    Category.FUNCTION_LIT: function_lit.generate_prompt,
    Category.FUNCTION_SCI_SS: function_sci_ss.generate_prompt,
    Category.PURPOSE_LIT: purpose_lit.generate_prompt,
    Category.PURPOSE_SCI_SS: purpose_sci_ss.generate_prompt,
}


def get_template(category):
    return ChatPromptTemplate(
        messages=[HumanMessagePromptTemplate.from_template(PROMPTS[category])],
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
    function_category_preprocess.FUNCTION_CATEGORY_PREPROCESS_PROMPT
)
