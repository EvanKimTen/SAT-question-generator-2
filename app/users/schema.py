from app.users.model import User
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel


UserData = pydantic_model_creator(User, name="UserData")

UserCreateInputBase = pydantic_model_creator(
    User,
    name="UserCreateInputBase",
    exclude_readonly=True,
)


class UserCreateInput(BaseModel):
    username: str
    password: str
    role: str

    class Config:
        title = "UserCreateInput"


class CurrentUserData(UserData):
    class Config:
        title = "CurrentUserData"
