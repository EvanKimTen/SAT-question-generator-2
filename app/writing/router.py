from fastapi import APIRouter, Depends, Header
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

router = APIRouter(prefix="/writing", tags=["Writing"])
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Just for getting 'access_token' and 'refresh_token' for testing.
data = supabase.auth.sign_in_with_password(
    {"email": "junhabin@gmail.com", "password": "jih4412*"}
)
print(supabase.auth.get_session())


@router.post("/problem_generation", response_model=List[CompleteGeneratedQuestion])
async def generate_similar_problem(
    request: GenerateSimilarQuestionRequest,
    access_token: str = Header(None),
    refresh_token: str = Header(None),
):
    results = await writing_service.generate_problems(
        request, supabase, access_token, refresh_token
    )
    return results


@router.post("/problem_set_generation", response_model=CompleteProblemSet)
async def problem_set_generation(
    request: GenerateProblemSetRequest,
    access_token: str = Header(None),
    refresh_token: str = Header(None),
):
    result = await writing_service.generate_problem_set(
        request, supabase, access_token, refresh_token
    )
    return result
