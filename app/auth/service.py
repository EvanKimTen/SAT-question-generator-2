from app.auth.schema import AuthLoginData
from app.auth.util import create_access_token, decode_token, verify_password
from app.users import service as user_service
from app.users.model import User
from fastapi import Depends, HTTPException
from fastapi import status as http_status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def authenticate(form_data: OAuth2PasswordRequestForm):
    user = await User.get(username=form_data.username)
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST, detail="Invalid password"
        )

    access_token = create_access_token(user.id)

    return AuthLoginData(access_token=access_token)


def get_current_user_authorizer(*, required: bool = True):  # type: ignore
    return get_current_user if required else get_current_user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
):
    token_payload = decode_token(token)
    user = await user_service.get(token_payload["user_id"])
    return user
