from pydantic import BaseModel, conint, Field
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class Category(str, Enum):
    FUNCTION_LIT = "Function - Literature"
    FUNCTION_SCI_SS = "Function - Sci / SS"
    PURPOSE_SCI_SS = "Purpose - Sci / SS"
    PURPOSE_LIT = "Purpose - Literature"

class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "Multiple Choice"


class ModelVersion(Enum):
    V1 = "v1"
    V2 = "v2"
    V3 = "v3"


class GenerateSimilarQuestionRequest(BaseModel):
    category: Category
    example_question: Optional[str]
    question_count: conint(ge=1, le=5) = Field(example=1)

class GenerateProblemSetRequest(BaseModel):
    category: Category
    question_count: conint(ge=1, le=5) = Field(example=1)


class GenerateTestSetRequest(BaseModel):
    category: Category
    question_count: conint(ge=1, le=5) = Field(example=1)


class GeneratedQuestion(BaseModel):
    question: str
    choice_a: str
    choice_b: str
    choice_c: str
    choice_d: str
    correct_choice: str
    solution: str

    
class SolutionWithChoices(BaseModel):
    choice_a: str
    choice_b: str
    choice_c: str
    choice_d: str
    correct_choice: str
    solution: str


class CompleteGeneratedQuestion(BaseModel):
    passage: str = Field(
        description="selected passage with one underlined passage ($\\underbar{{}}$)"
    )
    question: str
    choice_a: str
    choice_b: str
    choice_c: str
    choice_d: str
    correct_choice: str
    solution: str

class CompleteProblemSet(BaseModel):
    id: int
    question: str
    explanation: str

class CompleteTestSet(BaseModel):
    question: str
    explanation: str
    
class Module(str, Enum):
    INITIAL = "1"
    NEXT_EASY = "2-easy"
    NEXT_HARD ="2-hard"


class PreprocessedPassage(BaseModel):
    preprocessed_passage: str