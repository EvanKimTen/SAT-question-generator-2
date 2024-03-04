from fastapi import APIRouter, Header
from app.test_gen import service as test_service
from app.test_gen.schema import CompleteTestSet
from supabase import Client, create_client
from app.constants import SUPABASE_URL, SUPABASE_KEY

router = APIRouter(prefix="/test_gen", tags=["Test"])
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@router.post(
    "/test_generation", response_model=CompleteTestSet
) 
async def test_generation(
    access_token: str = Header(None),
    refresh_token: str = Header(None),
):
    # results = test_service.generate_test(supabase)
    results = test_service.generate_test(supabase, access_token, refresh_token)
    return results