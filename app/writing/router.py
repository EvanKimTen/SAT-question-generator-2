from fastapi import APIRouter, HTTPException

from app.writing.schemas import (
    GenerateSimilarQuestionRequest,
    CompleteGeneratedQuestion,
    Category,
    QuestionType,
    ModelVersion,
)
from typing import List
from supabase import create_client, Client

router = APIRouter(prefix="/writing", tags=["Writing"])

from app.writing import service as writing_service
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
    results = writing_service.generate_questions(request)
    return results

    
@router.post(
    "/problem_set_generation", response_model=List[CompleteGeneratedQuestion]
) 
async def problem_set_generation(
    request: GenerateSimilarQuestionRequest,
):
    result = writing_service.generate_problem_set(request)
    return result

@router.post(
    "/test_generation", response_model=List[CompleteGeneratedQuestion]
) 
async def test_generation(
    request: GenerateSimilarQuestionRequest,
    # current_user = Depends(get_current_user_authorizer()),
): # parameter: undecided.
    result = writing_service.generate_test(request)
    return result