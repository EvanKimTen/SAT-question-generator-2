from typing import Generic, Optional, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel
from enum import Enum


class Error(BaseModel):
    code: int
    message: str


DataT = TypeVar("DataT")


class ResponseSchema(GenericModel, Generic[DataT]):
    data: Optional[DataT] or None
    error: Optional[Error] or None

    def ok(self):
        return self

    def body(self, data):
        self.data = data
        return self


class ModelVersion(str, Enum):
    V1 = "v1"
    V2 = "v2"
    V3 = "v3"


class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "Multiple Choice"
    SHORT_ANSWER = "Short Answer"


class Subject(str, Enum):
    MATH = "MATH"
    ENGLISH = "ENGLISH"


class Module(str, Enum):
    FIRST_SESSION = "1"
    SECOND_SESSION_EASY = "2-easy"
    SECOND_SESSION_HARD = "2-hard"
