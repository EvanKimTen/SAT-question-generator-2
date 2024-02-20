from fastapi import APIRouter
from supabase import create_client, Client
from app.writing.schemas import (
    GenerateSimilarQuestionRequest,
    GenerateTestSetRequest,
    CompleteGeneratedQuestion,
)
from typing import List

from app.constants import SUPABASE_URL, SUPABASE_KEY

router = APIRouter(prefix="/writing", tags=["Writing"])

from app.writing import service as writing_service

supabase_exp: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@router.post(
    "/problem_generation", response_model=List[CompleteGeneratedQuestion]
) 
async def generate_similar_question(
    request: GenerateSimilarQuestionRequest,
    # current_user = Depends(get_current_user_authorizer()),
):
    results = writing_service.generate_questions(request, supabase_exp)
    return results

    
@router.post(
    "/problem_set_generation", response_model=List[CompleteGeneratedQuestion]
) 
async def problem_set_generation(
    request: GenerateSimilarQuestionRequest,
):
    result = writing_service.generate_problem_set(request, supabase_exp)
    return result

@router.post(
    "/test_generation", response_model=List[CompleteGeneratedQuestion]
) 
async def test_generation(
    request: GenerateTestSetRequest,
    # current_user = Depends(get_current_user_authorizer()),
): # parameter: undecided.
    result = writing_service.generate_test(request, supabase_exp)
    return result