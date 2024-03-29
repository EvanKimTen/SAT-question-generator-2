from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from app.writing.parsers import complete_generated_question_parser
from app.writing.schemas import Category
from app.writing.prompts import (
    accomplishing_the_goal,
    apostrophe,
    modifier_subject,
    parallel_structure,
    subject_verb_agreement,
    transitions,
    verb_forms,
    verb_tense,
    punctuations,
    sentence_fragment,
    essential_nonessential,
    pronoun,
    supplements,
    generic,
)
from app.db import supabase

PROMPTS = {
    Category.ACCOMPLISHING_THE_GOAL: accomplishing_the_goal.generate_prompt,
    Category.APOSTROPHE: apostrophe.generate_prompt,
    Category.SUBJECT_MODIFIER: modifier_subject.generate_prompt,
    Category.PARALLEL_STRUCTURE: parallel_structure.generate_prompt,
    Category.SUBJECT_VERB_AGREEMENT: subject_verb_agreement.generate_prompt,
    Category.TRANSITIONS: transitions.generate_prompt,
    Category.VERB_FORMS: verb_forms.generate_prompt,
    Category.VERB_TENSE: verb_tense.generate_prompt,
    Category.PUNCTUATIONS: punctuations.generate_prompt,
    Category.SENTENCE_FRAGMENT: sentence_fragment.generate_prompt,
    Category.ESSENTIAL_NONESSENTIAL: essential_nonessential.generate_prompt,
    Category.PRONOUN: pronoun.generate_prompt,
    Category.SUPPLEMENTS: supplements.generate_prompt,
    'generic': generic.generate_prompt,
}


def get_template(category_id):
    category = supabase.from_("problem_categories").select("generate_prompt").eq("id", category_id).execute()
    generate_prompt = category.data[0]["generate_prompt"]

    if generate_prompt is None:
        generate_prompt = generic.generate_prompt
    print('generate_prompt: ', generate_prompt)
    return ChatPromptTemplate(
        messages=[HumanMessagePromptTemplate.from_template(generate_prompt)],
        input_variables=["example_question", "question_type"],
        partial_variables={
            "format_instructions": complete_generated_question_parser.get_format_instructions()
        },
    )
