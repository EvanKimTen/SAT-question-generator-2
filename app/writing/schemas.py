from pydantic import BaseModel, conint, Field
from enum import Enum
from typing import Optional


class Category(str, Enum):
    PUNCTUATIONS = "Punctuations"
    SENTENCE_FRAGMENT = "Sentence vs Fragment"
    ESSENTIAL_NONESSENTIAL = "Essential vs Non-Essential"
    APOSTROPHE = "Apostrophe"
    PRONOUN = "Pronoun: Case and Agreement"
    SUBJECT_VERB_AGREEMENT = "Subject-Verb Agreement"
    VERB_TENSE = "Verb Tense"
    VERB_FORMS = "Verb Forms"
    PARALLEL_STRUCTURE = "Parallel Structure" # 1
    SUBJECT_MODIFIER = "Subject-Modifier"
    TRANSITIONS = "Transitions" # 4
    ACCOMPLISHING_THE_GOAL = "Accomplishing the Goal" # 2


class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "Multiple Choice"


class ModelVersion(Enum):
    V1 = "v1"
    V2 = "v2"
    V3 = "v3"

class GenerateSimilarQuestionRequest(BaseModel):
    category: Category
    example_question: Optional[str]
    model_version: ModelVersion
    question_count: conint(ge=1, le=5) = Field(example=1)
    solution: Optional[str]

class GenerateTestSetRequest(BaseModel):
    category: Category
    example_question: Optional[str]
    question_count: conint(ge=1, le=5) = Field(example=1)
    model_version: ModelVersion

class Module(str, Enum):
    INITIAL = "1"
    NEXT_EASY = "2-easy"
    NEXT_HARD ="2-hard"

class GeneratedQuestion(BaseModel):
    question: str
    type: QuestionType


class SolutionWithChoices(BaseModel):
    choice_a: str
    choice_b: str
    choice_c: str
    choice_d: str
    correct_choice: str
    solution: str


class CompleteGeneratedQuestion(BaseModel):
    passage: Optional[str]
    question: str
    choice_a: Optional[str]
    choice_b: Optional[str]
    choice_c: Optional[str]
    choice_d: Optional[str]
    correct_choice: Optional[str]
    solution: Optional[str]

class CompleteProblemSet(BaseModel):
    question: str
    explanation: str

class CompleteTestSet(BaseModel):
    question: str
    explanation: str