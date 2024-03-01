from fastapi import APIRouter
from supabase import create_client, Client
from app.reading.schemas import (
    GenerateSimilarQuestionRequest,
    GenerateProblemSetRequest,
    CompleteGeneratedQuestion,
    CompleteProblemSet,
)
from typing import List

router = APIRouter(prefix="/reading", tags=["Reading"])

from app.constants import SUPABASE_URL, SUPABASE_KEY
from app.reading import service as reading_service


supabase_exp: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@router.post(
    "/problem_generation", response_model=List[CompleteGeneratedQuestion]
)
async def generate_similar_problem(
    request: GenerateSimilarQuestionRequest,
    # current_user = Depends(get_current_user_authorizer()),
):
    result = reading_service.generate_problems(request, supabase_exp)
    return result

@router.post(
    "/problem_set_generation", response_model=List[CompleteProblemSet]
) 
async def problem_set_generation(
    request: GenerateProblemSetRequest,
):
    result = reading_service.generate_problem_set(request, supabase_exp)
    return result
