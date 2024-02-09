from fastapi import APIRouter
from app.math.schemas import (
    GenerateSimilarQuestionRequest,
    CompleteGeneratedQuestion,
    MajorCategory,
    QuestionType,
    ModelVersion,
    SolveQuestionSympyRequest,
    SympySolvedQuestion,
)

from typing import List

router = APIRouter(prefix="/math", tags=["Math"])

@router.post(
    "/generate-questions", response_model=List[CompleteGeneratedQuestion]
    )
async def generate_similar_question(
    request: GenerateSimilarQuestionRequest,
    ):
    result = generate_question(request)
    return result