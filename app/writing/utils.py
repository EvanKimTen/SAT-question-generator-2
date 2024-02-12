from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
)
from app.writing.templates import get_template
from app.writing.parsers import complete_generated_question_parser
from app.writing.schemas import QuestionType, Category
from app.constants import OPENAI_API_KEY


model_name = "gpt-3.5-turbo-0613"
chat_model = ChatOpenAI(
    model_name=model_name, openai_api_key=OPENAI_API_KEY, max_tokens=1000
)


def inference_with_chatcompletion_model(prompt: str, model_name: str):
    chat = ChatOpenAI(model_name=model_name, openai_api_key=OPENAI_API_KEY)
    messages = [HumanMessage(content=prompt)]
    return chat(messages)


def generate_sat_question(
    category: Category,
    example_question: str,
):
    _input = get_template(category).format_prompt(
        category=category,
        example_question=example_question,
    )
    output = chat_model(_input.to_messages())
    res = complete_generated_question_parser.parse(output.content)
    return res