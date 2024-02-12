from fastapi import APIRouter, Depends
from supabase import create_client, Client
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

from app.math import service as math_service

SUPABASE_URL: str = "your_supabase_url"
SUPABASE_KEY: str = "your_supabase_key"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@router.post(
    "/problem_generation", response_model=List[CompleteGeneratedQuestion]
)
async def generate_similar_question(
    request: GenerateSimilarQuestionRequest,
    # current_user = Depends(get_current_user_authorizer()),
):
    result = math_service.generate_questions(request)
    return result

@router.post(
    "/problem_set_generation", response_model=List[CompleteGeneratedQuestion]
)
async def generate_similar_question(
    request: GenerateSimilarQuestionRequest,
    # current_user = Depends(get_current_user_authorizer()),
):
    result = math_service.generate_problem_set(request)
    return result

@router.post(
    "/test_set_generation", response_model=List[CompleteGeneratedQuestion]
)
async def generate_similar_question(
    request: GenerateSimilarQuestionRequest,
    # current_user = Depends(get_current_user_authorizer()),
):
    result = math_service.generate_test_set(request)
    return result