import asyncpg
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.repositories.repository import UserRepository
from src.app.schemas.users import SUserCreate, SUser, SUserId, SUserLockResp, SUserLockAdd
from src.database import get_async_session

router = APIRouter(
    tags=["Users"]
)

message_500 = "Unexpected error"


@router.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(user: SUserCreate, session: AsyncSession = Depends(get_async_session)) -> SUserId:
    user_id, err = await UserRepository.add_one(user, session)
    if err is None:
        return SUserId(user_id=user_id)

    match err:
        case asyncpg.UniqueViolationError:
            message = f"User with login {user.login} is already exist!"
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=message)

        case _:
            raise HTTPException(status_code=500, detail=message_500)


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_users(session: AsyncSession = Depends(get_async_session)) -> list[SUser]:
    users = await UserRepository.get_all(session)
    return users


@router.put("/user/lock", status_code=status.HTTP_201_CREATED)
async def acquire_lock(user_id: SUserLockAdd, session: AsyncSession = Depends(get_async_session)) -> SUserLockResp:
    locked, err = await UserRepository.lock(user_id, session)
    if err is None:
        return locked

    match err:
        case asyncpg.NoData:

            raise HTTPException(status_code=404, detail="User not found")
        case asyncpg.LockNotAvailableError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User have already blocked in {locked}")
        case _:
            raise HTTPException(status_code=500, detail=message_500)


@router.put("/user/unlock", status_code=status.HTTP_201_CREATED)
async def release_lock(user_id: SUserLockAdd, session: AsyncSession = Depends(get_async_session)) -> SUserLockResp:
    locked, err = await UserRepository.unlock(user_id, session)
    if err is None:
        return locked

    match err:
        case asyncpg.NoData:
            raise HTTPException(status_code=404, detail="User not found")
        case asyncpg.LockNotAvailableError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User have already unblocked")
        case _:
            raise HTTPException(status_code=500, detail=message_500)
