from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
)
from app.reading.templates import get_template, function_category_preprocess_prompt
from app.reading.parsers import generated_question_parser
from app.reading.schemas import Category, CompleteGeneratedQuestion
from app.core.utils import generate_category_string

from app.reading.prompts.fix_json_parsing import JSON_FORMAT_FIX_PROMPT
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import re
from langchain.embeddings import OpenAIEmbeddings
import random
from supabase import create_client, Client
import json
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# model_name = "gpt-3.5-turbo-16k-0613"
model_name = "gpt-4-turbo-preview"
chat_model = ChatOpenAI(
    model_name=model_name,
    openai_api_key=OPENAI_API_KEY,
    max_tokens=2000,
    model_kwargs={"response_format": {"type": "json_object"}},
)
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)


def inference_with_chatcompletion_model(prompt: str, model_name: str):
    chat = ChatOpenAI(model_name=model_name, openai_api_key=OPENAI_API_KEY)
    messages = [HumanMessage(content=prompt)]
    return chat(messages)


async def generate_sat_question(
    category_id: str,
    example_question: str,
    user_id: str,
    display_id: str,
    selection_passage_example: str = None,
) -> CompleteGeneratedQuestion:
    """
    Two Step Generation:
    Step 1. Select a passage from the text.
    Step 2. Generate a question based off the passage selected.
    """
    selected_passages = (
        supabase.table("reading_passage").select("passage, source_title").execute()
    )
    selected_row = random.choice(selected_passages.data)
    selected_passage = selected_row["passage"]
    source_title = selected_row["source_title"]

    category_string = await generate_category_string([category_id])

    # Preprocess the selected passage if the category is FUNCTION_LIT or FUNCTION_SCI_SS (Underline the sentence in the passage.)
    if category_id == Category.FUNCTION_LIT or category_id == Category.FUNCTION_SCI_SS:
        # using langchain to underline the sentence, use FUNCTION_CATEGORY_PREPROCESS_PROMPT
        _input = function_category_preprocess_prompt.format_prompt(
            passage=selected_passage
        )
        output = chat_model(_input.to_messages())
        selected_passage = json.loads(output.content)["preprocessed_passage"]

    _input = get_template(category_id).format_prompt(
        category=category_string,
        example_question=example_question,
        selected_passage=selected_passage,
        source_title=source_title,
    )
    output = chat_model(_input.to_messages())
    output = preprocess_output(output.content)

    try:
        res = generated_question_parser.parse(output)
    except Exception as e:
        print("error occurred..")
        print(str(e))
        llm = ChatOpenAI
        chain = LLMChain(llm=llm, prompt=JSON_FORMAT_FIX_PROMPT)
        res = chain.run(bad_response=output, error_msg=str(e))
    # add selected_passage to the response
    res_dict = res.dict()

    res_dict["passage"] = selected_passage
    res_dict["user_id"] = user_id
    res_dict["display_id"] = display_id
    

    generated_problem = (
        supabase.table("problems").select("*").match(res_dict).execute()
    )  # using this table for experiment and be adjusted for the correct one
    generated_problem_id = generated_problem.data[0]["id"]
    supabase.table("problem_problem_categories").insert(
        {
            "problem_id": generated_problem_id,
            "category_id": category_id,
        }
    ).execute()

    complete_generated_question = CompleteGeneratedQuestion.parse_obj(res_dict)

    return complete_generated_question


def preprocess_output(string):
    string = make_escape_pairs(string)
    string = string.replace('\\"', "")
    string = preprocess_string(string)
    return string


def make_escape_pairs(string):
    pattern = r"(?<!\\)(\\\\)*\\(?!\\)"
    return re.sub(pattern, r"\\\\", string)


def preprocess_string(input_string):
    # Encode the string to bytes
    encoded_string = input_string.encode("unicode_escape")

    # Decode the bytes with errors='backslashreplace' to replace invalid escapes
    processed_string = encoded_string.decode(
        "unicode_escape", errors="backslashreplace"
    )

    return processed_string
