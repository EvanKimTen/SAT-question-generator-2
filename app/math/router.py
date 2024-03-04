from fastapi import APIRouter, Header
from supabase import create_client, Client
from app.math.schemas import (
    GenerateSimilarQuestionRequest,
    GenerateProblemSetRequest,
    GenerateTestSetRequest,
    CompleteGeneratedQuestion,
    CompleteProblemSet,
)
from typing import List
router = APIRouter(prefix="/math", tags=["Math"])

from app.math import service as math_service
from app.constants import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@router.post(
    "/problem_generation", response_model=List[CompleteGeneratedQuestion]
)
async def generate_similar_problem(
    request: GenerateSimilarQuestionRequest,
    access_token: str = Header(None),
    refresh_token: str = Header(None)
    # current_user = Depends(get_current_user_authorizer()),
):
    result = math_service.generate_problems(request, supabase, access_token, refresh_token)
    return result

@router.post(
    "/problem_set_generation", response_model=CompleteProblemSet
)
async def problem_set_generation(
    request: GenerateProblemSetRequest,
    access_token: str = Header(None),
    refresh_token: str = Header(None)
    # current_user = Depends(get_current_user_authorizer()),
):
    result = math_service.generate_problem_set(request, supabase, access_token, refresh_token)
    return result
