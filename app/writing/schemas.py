from pydantic import BaseModel, conint, Field
from enum import Enum
from typing import Optional


class Category(str, Enum):
    PUNCTUATIONS = "Punctuations"  #
    SENTENCE_FRAGMENT = "Sentence vs Fragment"  #
    ESSENTIAL_NONESSENTIAL = "Essential vs Non-Essential"
    APOSTROPHE = "Apostrophe"  #
    PRONOUN = "Pronoun-Antecedent Agreement"  #
    SUBJECT_VERB_AGREEMENT = "Subject-Verb Agreement"  #
    VERB_TENSE = "Verb Forms - Tense"  #
    VERB_FORMS = "Verb forms - Finite vs. Non-finite"  #
    PARALLEL_STRUCTURE = "Parallel Structure"  #
    SUBJECT_MODIFIER = "Subject-Modifier Placement"  #
    TRANSITIONS = "Transitions"  #
    SUPPLEMENTS = "Supplements"  #
    ACCOMPLISHING_THE_GOAL = "Accomplishing the Goal"  #


class CategoryLv2(str, Enum):
    PUNCTUATIONS = "Punctuations"
    SENTENCE_FRAGMENT = "Sentence vs Fragment"
    ESSENTIAL_NONESSENTIAL = "Essential vs Non-Essential"
    APOSTROPHE = "Apostrophe"
    PRONOUN = "Pronoun: Case and Agreement"
    SUBJECT_VERB_AGREEMENT = "Subject-Verb Agreement"
    VERB_TENSE = "Verb Tense"
    VERB_FORMS = "Verb Forms"
    PARALLEL_STRUCTURE = "Parallel Structure"
    SUBJECT_MODIFIER = "Subject-Modifier"
    TRANSITIONS = "Transitions"
    ACCOMPLISHING_THE_GOAL = "Accomplishing the Goal"


class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "Multiple Choice"


class GenerateSimilarQuestionRequest(BaseModel):
    category_id: str
    question_count: conint(ge=1, le=5) = Field(example=1)


class GenerateProblemSetRequest(BaseModel):
    category_id: str
    question_count: conint(ge=1, le=5) = Field(example=1)


class Module(str, Enum):
    INITIAL = "1"
    NEXT_EASY = "2-easy"
    NEXT_HARD = "2-hard"


class GeneratedQuestion(BaseModel):
    id: int
    question: str
    explanation: str


class SolutionWithChoices(BaseModel):
    choice_a: str
    choice_b: str
    choice_c: str
    choice_d: str
    answer: str
    solution: str


class CompleteGeneratedQuestion(BaseModel):
    passage: Optional[str]
    question: str
    choice_a: str
    choice_b: str
    choice_c: str
    choice_d: str
    answer: str
    explanation: str


class CompleteProblemSet(BaseModel):
    id: int
    name: str = Field(default="New Problem Set")
    is_full_test: bool
