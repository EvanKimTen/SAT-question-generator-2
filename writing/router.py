from fastapi import APIRouter, Depends
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
from app.auth.service import get_current_user_authorizer


@router.post(
    "/generate-similar-question", response_model=List[CompleteGeneratedQuestion]
)
async def generate_similar_question(
    request: GenerateSimilarQuestionRequest,
    # current_user = Depends(get_current_user_authorizer()),
):
    result = writing_service.generate_questions(request)
    return result


@router.get("/categories", response_model=List[Category])
async def get_categories():
    result = writing_service.get_category_list()
    return result


@router.get("/question-types", response_model=List[QuestionType])
async def get_question_types():
    result = writing_service.get_question_type_list()
    return result


@router.get("/model-versions", response_model=List[ModelVersion])
async def get_model_versions():
    result = writing_service.get_model_version_list()
    return result
