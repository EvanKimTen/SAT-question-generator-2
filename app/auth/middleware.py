from app.auth.util import decode_token
from fastapi import HTTPException
from fastapi.security.utils import get_authorization_scheme_param
from starlette.authentication import AuthCredentials, AuthenticationBackend, BaseUser
from starlette.status import HTTP_401_UNAUTHORIZED


class AuthenticatedUser(BaseUser):
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id

    @property
    def is_authenticated(self) -> bool:
        return True


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        if "Authorization" not in conn.headers:
            return

        try:
            scheme, credentials = get_authorization_scheme_param(
                conn.headers["Authorization"]
            )
            if scheme.lower() != "bearer":
                return
        except:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )

        payload = decode_token(credentials)

        return AuthCredentials(["authenticated"]), AuthenticatedUser(payload["user_id"])
