from app.auth import service as auth_service
from app.auth.schema import AuthLoginData
from app.core.schema import ResponseSchema
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Authorization"],
)


@router.post(
    "/login", response_model=ResponseSchema[AuthLoginData], operation_id="auth_login"
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    res = await auth_service.authenticate(form_data)

    return ResponseSchema[AuthLoginData]().ok().body(res)
