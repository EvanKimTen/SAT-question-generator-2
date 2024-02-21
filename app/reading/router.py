from fastapi import APIRouter
from app.reading.schemas import (
    GenerateSimilarQuestionRequest,
    CompleteGeneratedQuestion,
)
from typing import List

router = APIRouter(prefix="/reading", tags=["Reading"])

from app.reading import service as reading_service

@router.post(
    "/generate-similar-question", response_model=List[CompleteGeneratedQuestion]
)
async def generate_similar_question(
    request: GenerateSimilarQuestionRequest,
    # current_user = Depends(get_current_user_authorizer()),
):
    result = reading_service.generate_questions(request)
    return result

