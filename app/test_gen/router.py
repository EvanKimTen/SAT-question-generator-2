from fastapi import APIRouter, Header
from app.test_gen import service as test_service
from app.test_gen.schema import CompleteTestProblemSet

from supabase import Client, create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

router = APIRouter(prefix="/test_gen", tags=["Test"])
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@router.post("/test_generation", response_model=CompleteTestProblemSet)
async def test_generation(
    access_token: str = Header(None),
    refresh_token: str = Header(None),
):
    # results = test_service.generate_test(supabase)
    results = await test_service.generate_test(supabase, access_token, refresh_token)
    return results
