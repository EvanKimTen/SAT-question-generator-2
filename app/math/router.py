from fastapi import APIRouter, Depends
from supabase import create_client, Client
from app.math.schemas import (
    GenerateSimilarQuestionRequest,
    GenerateProblemSetRequest,
    GenerateTestSetRequest,
    CompleteGeneratedQuestion,
    ProblemInsideSet,
    CompleteTestSet,
    MajorCategory,
    QuestionType,
    ModelVersion,
    SolveQuestionSympyRequest,
    SympySolvedQuestion,
)
from typing import List

router = APIRouter(prefix="/math", tags=["Math"])

from app.math import service as math_service
from app.constants import SUPABASE_URL, SUPABASE_KEY

supabase_exp = create_client(SUPABASE_URL, SUPABASE_KEY)

@router.post(
    "/problem_generation", response_model=List[CompleteGeneratedQuestion]
)
async def generate_similar_question(
    request: GenerateSimilarQuestionRequest,
    # current_user = Depends(get_current_user_authorizer()),
):
    result = math_service.generate_questions(request, supabase_exp)
    return result

@router.post(
    "/problem_set_generation", response_model=List[ProblemInsideSet]
)
async def generate_similar_question(
    request: GenerateProblemSetRequest,
    # current_user = Depends(get_current_user_authorizer()),
):
    result = math_service.generate_problem_set(request, supabase_exp)
    return result

@router.post(
    "/test_set_generation", response_model=List[CompleteTestSet]
)
async def generate_similar_question(
    request: GenerateTestSetRequest,
    # current_user = Depends(get_current_user_authorizer()),
):
    result = math_service.generate_test_set(request, supabase_exp)
    return result