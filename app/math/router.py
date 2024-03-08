from fastapi import APIRouter, Header, HTTPException
from supabase import create_client, Client
from app.math.schemas import (
    GenerateSimilarQuestionRequest,
    GenerateProblemSetRequest,
    CompleteGeneratedQuestion,
    CompleteProblemSet,
)
from typing import List

router = APIRouter(prefix="/math", tags=["Math"])

from app.math import service as math_service
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@router.post("/problem_generation", response_model=List[CompleteGeneratedQuestion])
async def generate_similar_problem(
    request: GenerateSimilarQuestionRequest,
    access_token: str = Header(None),
    refresh_token: str = Header(None)
    # current_user = Depends(get_current_user_authorizer()),
):
    try:
        result = await math_service.generate_problems(
            request, supabase, access_token, refresh_token
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/problem_set_generation", response_model=CompleteProblemSet)
async def problem_set_generation(
    request: GenerateProblemSetRequest,
    access_token: str = Header(None),
    refresh_token: str = Header(None),
):
    try:
        result = await math_service.generate_problem_set(
            request, supabase, access_token, refresh_token
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
