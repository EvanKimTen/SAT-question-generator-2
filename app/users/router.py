from app.auth.service import get_current_user_authorizer
from app.core.schema import ResponseSchema
from app.users import service as user_service
from app.users.schema import CurrentUserData, UserCreateInput, UserData
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@router.get(
    "/me",
    response_model=ResponseSchema[CurrentUserData],
    operation_id="get_current_user",
)
async def get_current_user(
    current_user: UserData = Depends(get_current_user_authorizer()),
):
    res_user = await user_service.get_by_current_user(current_user)
    return ResponseSchema[CurrentUserData]().ok().body(res_user)


@router.get("/{user_id}", response_model=ResponseSchema[UserData])
async def get_user(user_id: int):
    res_user = await user_service.get(user_id)
    return ResponseSchema[UserData]().ok().body(res_user)


@router.post("", response_model=ResponseSchema[UserData])
async def create(user: UserCreateInput):
    res_user = await user_service.create(user)
    return ResponseSchema[UserData]().ok().body(res_user)


@router.put("/{user_id}", response_model=ResponseSchema[int])
async def update(user_id: int, user: UserCreateInput):
    res_user = await user_service.update(user_id, user)
    return ResponseSchema[UserData]().ok().body(res_user)


@router.delete("/{user_id}", response_model=ResponseSchema[int])
async def delete(user_id: int):
    res_user = await user_service.delete(user_id)
    return ResponseSchema[int]().ok().body(res_user)
