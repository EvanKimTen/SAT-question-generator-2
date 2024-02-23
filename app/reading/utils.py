from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
)
from app.reading.templates import get_template, function_category_preprocess_prompt
from app.reading.parsers import generated_question_parser
from app.reading.schemas import Category, CompleteGeneratedQuestion

from app.reading.prompts.fix_json_parsing import JSON_FORMAT_FIX_PROMPT
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import re
from langchain.embeddings import OpenAIEmbeddings
from app.constants import OPENAI_API_KEY, SUPABASE_URL, SUPABASE_KEY


from typing import List
import random
from supabase import create_client, Client
import json

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# model_name = "gpt-3.5-turbo-16k-0613"
model_name = "gpt-4-turbo-preview"
chat_model = ChatOpenAI(
    model_name=model_name, openai_api_key=OPENAI_API_KEY, max_tokens=2000, model_kwargs={"response_format":{ "type": "json_object" }},
)
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

def inference_with_chatcompletion_model(prompt: str, model_name: str):
    chat = ChatOpenAI(model_name=model_name, openai_api_key=OPENAI_API_KEY)
    messages = [HumanMessage(content=prompt)]
    return chat(messages)


def generate_sat_question_old(
    category: Category,
    example_question: str,
    selected_namespaces: List[str],
    selection_passage_example: str,
):
    """
    One Step Generation:
    Generate a question by directly querying pinecone.
    """
    source_title = random.choice(selected_namespaces)
    _input = old_templates.get_template(category).format_prompt(
        category=category,
        example_question=example_question,
    )

    output = query_pinecone(query=_input.to_string(), selected_namespace=source_title)
    output = preprocess_output(output)

    try:
        res = complete_generated_question_parser.parse(output)
    except Exception as e:
        print("error occurred..")
        print(str(e))
        llm = ChatOpenAI
        chain = LLMChain(llm=llm, prompt=JSON_FORMAT_FIX_PROMPT)
        res = chain.run(bad_response=output, error_msg=str(e))

    return res


def generate_sat_question(
    category: Category,
    example_question: str,
    selection_passage_example: str = None,
) -> CompleteGeneratedQuestion:
    """
    Two Step Generation:
    Step 1. Select a passage from the text.
    Step 2. Generate a question based off the passage selected.
    """
    selected_passages = supabase.table("reading_passage").select("passage, source_title").execute()
    selected_row = random.choice(selected_passages.data)
    selected_passage = selected_row["passage"]
    source_title = selected_row["source_title"]
    
    # Preprocess the selected passage if the category is FUNCTION_LIT or FUNCTION_SCI_SS (Underline the sentence in the passage.)
    if category == Category.FUNCTION_LIT or category == Category.FUNCTION_SCI_SS:
        # using langchain to underline the sentence, use FUNCTION_CATEGORY_PREPROCESS_PROMPT
        _input = function_category_preprocess_prompt.format_prompt(
            passage=selected_passage
        )
        output = chat_model(_input.to_messages())
        selected_passage = json.loads(output.content)["preprocessed_passage"]
    _input = get_template(category).format_prompt(
        category=category,
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
    res_dict['passage'] = selected_passage
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


if __name__ == "__main__":
    model_name = "gpt-3.5-turbo-0613"

    category = Category.FUNCTION_LIT
    question = """Question: Despite his busy schedule, John managed to complete all his assignments on time. ___________, he even had time to help his classmates with their projects.
A) Consequently,
B) Nevertheless,
C) Furthermore,
D) However,

Correct Answer: C) Furthermore,"""
    generated_question = generate_sat_question(
        category=category,
        example_question=""
    )
    print(generated_question)
