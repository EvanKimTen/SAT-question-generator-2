from pydantic import BaseModel, Field
from uuid import UUID
from typing import List

class GeneratedQuestion(BaseModel):
    id: int
    question: str

class CompleteTestSet(BaseModel):
    name: str = Field(default="New Test")
    is_full_test: bool = Field(example=True)
    # user_id: UUID
    set: List[GeneratedQuestion]