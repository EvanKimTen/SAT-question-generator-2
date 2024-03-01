from fastapi import APIRouter, Depends
from app.test_gen import service as test_service
from app.test_gen.schema import CompleteTestSet
from app.auth.service import get_current_user_authorizer
from supabase import Client, create_client
from app.constants import SUPABASE_URL, SUPABASE_KEY
from app.users.schema import CurrentUserData, UserCreateInput, UserData

router = APIRouter(prefix="/test", tags=["Test"])
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@router.post(
    "/test_generation", response_model=CompleteTestSet
) 
async def test_generation(
    supabase = Client,
    current_user: UserData = Depends(get_current_user_authorizer())
):
    results = test_service.generate_test(supabase, current_user)
    return results