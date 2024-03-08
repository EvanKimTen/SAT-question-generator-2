from fastapi import APIRouter, Header, HTTPException
from supabase import create_client, Client
from app.reading.schemas import (
    GenerateSimilarQuestionRequest,
    GenerateProblemSetRequest,
    CompleteGeneratedQuestion,
    CompleteProblemSet,
)
from typing import List

router = APIRouter(prefix="/reading", tags=["Reading"])

from app.reading import service as reading_service
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


supabase_exp: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@router.post("/problem_generation", response_model=List[CompleteGeneratedQuestion])
async def generate_similar_problem(
    request: GenerateSimilarQuestionRequest,
    access_token: str = Header(None),
    refresh_token: str = Header(None),
):
    # try:
    result = await reading_service.generate_problems(
        request, supabase_exp, access_token, refresh_token
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
        result = await reading_service.generate_problem_set(
            request, supabase_exp, access_token, refresh_token
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
