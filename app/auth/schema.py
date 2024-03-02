from pydantic import BaseModel


class AuthLoginData(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AuthTokenData(BaseModel):
    user_id: int
    username: str
