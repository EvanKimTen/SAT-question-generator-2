from fastapi import APIRouter

from app.writing.schemas import (
    GenerateSimilarQuestionRequest,
    CompleteGeneratedQuestion,
    Category,
    QuestionType,
    ModelVersion,
)
from typing import List
router = APIRouter(prefix="/writing", tags=["Writing"])

from app.writing import service as writing_service

@router.post(
    "/generate-questions", response_model=List[CompleteGeneratedQuestion]
) 
async def generate_similar_question(
    request: GenerateSimilarQuestionRequest,
    # current_user = Depends(get_current_user_authorizer()),
): # Basically, GenerateSimilarQuestionRequest --> CompleteGeneratedQuestion
    result = writing_service.generate_questions(request)
    return result
    
    