from pydantic import BaseModel, conint, Field
from enum import Enum
from pydantic import BaseModel


class Category(str, Enum):
    FUNCTION_LIT = "Function - Literature"
    FUNCTION_SCI_SS = "Function - Sci / SS"
    PURPOSE_SCI_SS = "Purpose - Sci / SS"
    PURPOSE_LIT = "Purpose - Literature"
    LITERARY_EVIDENCE = "Literary Evidence"


class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "Multiple Choice"


class GenerateSimilarQuestionRequest(BaseModel):
    category_id: str
    question_count: conint(ge=1, le=5) = Field(example=1)


class GenerateProblemSetRequest(BaseModel):
    category_id: str
    question_count: conint(ge=1, le=5) = Field(example=1)


class GeneratedQuestion(BaseModel):
    question: str
    choice_a: str
    choice_b: str
    choice_c: str
    choice_d: str
    answer: str
    explanation: str


class QuestionInsideSet(BaseModel):
    id: int
    question: str
    explanation: str


class SolutionWithChoices(BaseModel):
    choice_a: str
    choice_b: str
    choice_c: str
    choice_d: str
    answer: str
    explanation: str


class CompleteGeneratedQuestion(BaseModel):
    passage: str = Field(
        description="selected passage with one underlined passage ($\\underbar{{}}$)"
    )
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


class PreprocessedPassage(BaseModel):
    preprocessed_passage: str
