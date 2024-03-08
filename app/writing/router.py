from fastapi import APIRouter, Header, HTTPException
from app.writing.schemas import (
    GenerateSimilarQuestionRequest,
    GenerateProblemSetRequest,
    CompleteGeneratedQuestion,
    CompleteProblemSet,
)
from typing import List
from app.writing import service as writing_service
from app.db import supabase

router = APIRouter(prefix="/writing", tags=["Writing"])

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
    # try:
        result = await writing_service.generate_problems(
            request, access_token, refresh_token
        )
        return result
    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=str(e))


@router.post("/problem_set_generation", response_model=CompleteProblemSet)
async def problem_set_generation(
    request: GenerateProblemSetRequest,
    access_token: str = Header(None),
    refresh_token: str = Header(None),
):
    try:
        result = await writing_service.generate_problem_set(
            request, access_token, refresh_token
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
