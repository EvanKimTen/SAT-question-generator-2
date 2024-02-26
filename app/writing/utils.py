from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage, AIMessage
)
from app.writing.templates import get_template
from app.writing.parsers import complete_generated_question_parser
from app.writing.schemas import QuestionType, Category
from app.constants import OPENAI_API_KEY

import json

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
    category: Category,
    example_question: str,
):
    _input = get_template(category).format_prompt(
        category=category,
        example_question=example_question,
    )
    output = chat_model(_input.to_messages())
    # print(output.content)
    # print(output)
    res = complete_generated_question_parser.parse(output.content)
    return res


# def convert_ai_message_to_dict(ai_message):
#     # Extracting the content from the AI message
#     content = ai_message.content

#     # Parsing the content to create a dictionary
#     content = content[1:]
#     # Splitting the content into parts
#     parts = content.split('\n\n')
#     dict_output = {}

#     for part in parts:
#         if part.startswith('Passage:\n'):
#             dict_output['Passage'] = part[len('Passage:'):].strip()
#         elif part.startswith('Question:'):
#             dict_output['Question'] = part[len('Question:'):].strip()
#         elif part.startswith('Correct Answer:'):
#             dict_output['Correct Answer'] = part[len('Correct Answer:'):].strip()
#         elif part.startswith('A) '):
#             choices = part.split('\n')
#             dict_output['choice_a'] = choices[0][3:]
#             dict_output['choice_b'] = choices[1][3:]
#             dict_output['choice_c'] = choices[2][3:]
#             dict_output['choice_d'] = choices[3][3:]
#         elif part.startswith('Explanation:'):
#             dict_output['Explanation'] = part[len('Explanation:'):].strip()
#     dict_output = json.dumps(dict_output)
#     parsed_content = AIMessage(content = dict_output, example=False)     
#     return parsed_content