from fastapi import APIRouter, Depends
from supabase import create_client, Client
from app.writing.schemas import (
    GenerateSimilarQuestionRequest,
    GenerateProblemSetRequest,
    CompleteGeneratedQuestion,
    CompleteProblemSet,
)
from typing import List

from app.constants import SUPABASE_URL, SUPABASE_KEY
from app.writing import service as writing_service
from app.auth.service import get_current_user_authorizer
from app.users.schema import CurrentUserData, UserCreateInput, UserData

router = APIRouter(prefix="/writing", tags=["Writing"])
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@router.post(
    "/problem_generation", response_model=List[CompleteGeneratedQuestion]
) 
async def generate_similar_problem(
    request: GenerateSimilarQuestionRequest,
    
):
    results = writing_service.generate_problems(request, supabase)
    return results


@router.post(
    "/problem_set_generation", response_model=CompleteProblemSet
) 
async def problem_set_generation(
    request: GenerateProblemSetRequest,
):
    result = writing_service.generate_problem_set(request, supabase)
    return result