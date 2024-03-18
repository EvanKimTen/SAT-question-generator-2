from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from app.writing.templates import get_template
from app.core.utils import generate_category_string
from app.db import supabase
import json
from app.writing.schemas import CompleteGeneratedQuestion
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# only below two models are supported for json response
# model_name = "gpt-3.5-turbo-0125"
model_name = "gpt-4-turbo-preview"
chat_model = ChatOpenAI(
    model_name=model_name,
    openai_api_key=OPENAI_API_KEY,
    max_tokens=1000,
    model_kwargs={"response_format": {"type": "json_object"}},
)


def inference_with_chatcompletion_model(prompt: str, model_name: str):
    chat = ChatOpenAI(model_name=model_name, openai_api_key=OPENAI_API_KEY)
    messages = [HumanMessage(content=prompt)]
    return chat(messages)


async def generate_sat_question(
    category_id: str,
    example_question: str,
    user_id: str,
):
    category_string = await generate_category_string([category_id])

    _input = get_template(category_id).format_prompt(
        category=category_string,
        example_question=example_question,
    )
    output = chat_model(_input.to_messages())
    
    output_dict = output.dict()["content"]
    output_dict = json.loads(output_dict)
    output_dict["user_id"] = user_id
    # print(output_dict)
    # get the id of the generated question and insert it into the problem_problem_categories table.
    generated_problem = (
        supabase.table("problems").select("*").match(output_dict).execute()
    )  
    
    # using this table for experiment and be adjusted for the correct one
    generated_problem_id = generated_problem.data[0]["id"]
    supabase.table("problem_problem_categories").insert(
        {
            "problem_id": generated_problem_id,
            "category_id": category_id,
        }
    ).execute()

    complete_generated_question = CompleteGeneratedQuestion.parse_obj(output_dict)

    return complete_generated_question
