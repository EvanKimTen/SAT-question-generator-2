from app.auth.util import get_hashed_password
from app.users.model import User
from app.users.schema import CurrentUserData, UserCreateInput, UserData


async def get(user_id: int) -> UserData:
    user_data = await UserData.from_queryset_single(User.get(id=user_id))
    return user_data


async def get_by_current_user(current_user: CurrentUserData) -> CurrentUserData:
    return CurrentUserData(**current_user.dict())


async def create(user: UserCreateInput):
    user_dict_data = user.dict(exclude_unset=True)
    user_dict_data["password"] = get_hashed_password(user_dict_data["password"])
    new_user_data = await User.create(**user_dict_data)
    user_data = await UserData.from_tortoise_orm(new_user_data)

    return user_data


async def update(user_id: int, user: UserCreateInput):
    user_data = await User.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return user_data


async def delete(user_id: int):
    user_data = await User.filter(id=user_id).delete()
    return user_data
