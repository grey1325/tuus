from fastapi import APIRouter, Depends, HTTPException

from src.api.schemas import UserResponse, UserUpdate
from src.dependencies import get_user_service
from src.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    try:
        user = await user_service.get_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return user


@router.put("/{user_id}")
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    user_service: UserService = Depends(get_user_service),
):
    try:
        return await user_service.update_user(user_id, user_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{user_id}")
async def delete_user(
    user_id: int, user_service: UserService = Depends(get_user_service)
):
    try:
        await user_service.delete_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": f"Пользователь {user_id} удалён"}
