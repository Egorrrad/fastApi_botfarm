import datetime

import asyncpg
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.users import UserOrm
from src.app.schemas.users import SUserCreate, SUser, SUserLockAdd, SUserLockResp
from src.app.utils.users import hash_password


class UserRepository:
    @classmethod
    async def add_one(cls, data: SUserCreate, session: AsyncSession) -> (int, Exception):
        user_dict = data.model_dump()

        user: UserOrm = UserOrm(**user_dict)

        user.password = hash_password(user.password)

        query = select(UserOrm).where(UserOrm.login == user.login)
        result = await session.execute(query)
        user1: UserOrm = result.first()

        if user1:
            return 0, asyncpg.UniqueViolationError

        session.add(user)

        await session.flush()
        await session.commit()
        return user.id, None

    @classmethod
    async def get_all(cls, session) -> list[SUser]:
        query = select(UserOrm)
        result = await session.execute(query)
        user_models = result.scalars().all()
        user_shemas = [SUser.model_validate(user_orm) for user_orm in user_models]
        return user_shemas

    @classmethod
    async def lock(cls, data: SUserLockAdd, session) -> (SUserLockResp, bool):
        session: AsyncSession
        user_id = data.id
        user: UserOrm = await session.get(UserOrm, user_id)

        if not user:
            return None, asyncpg.NoData

        if user.locktime is None:
            user.locktime = datetime.datetime.now()
        else:
            return user.locktime, asyncpg.LockNotAvailableError

        await session.commit()

        user_locked = SUserLockResp(id=user_id, locktime=user.locktime, locked_yet=False)
        return user_locked, None

    @classmethod
    async def unlock(cls, data: SUserLockAdd, session) -> (SUserLockResp, bool):
        session: AsyncSession
        user_id = data.id

        user: UserOrm = await session.get(UserOrm, user_id)
        if not user:
            return None, asyncpg.NoData

        if user.locktime is None:
            return None, asyncpg.LockNotAvailableError

        user.locktime = None
        await session.commit()

        user_locked = SUserLockResp(id=user_id, locktime=user.locktime, locked_yet=False)
        return user_locked, None
