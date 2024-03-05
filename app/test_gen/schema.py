from pydantic import BaseModel, Field
from enum import Enum
from uuid import UUID
from typing import List
from app.core.schema import Module, Subject


class GeneratedQuestion(BaseModel):
    id: int
    question: str


class Test(BaseModel):
    name: str = Field(default="New Test")
    is_full_test: bool = Field(example=True)
    user_id: UUID


class CompleteTestProblem(BaseModel):
    test_id: int
    problem_id: int
    module: Module
    subject: Subject


class CompleteTestProblemSet(BaseModel):
    set: List[GeneratedQuestion]
