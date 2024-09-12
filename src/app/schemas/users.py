import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class SUserCreate(BaseModel):
    """ Проверяет sign up запрос """
    login: EmailStr
    password: str
    project_id: int
    env: str
    domain: str


class SUser(BaseModel):
    """ Формирует тело ответа с деталями пользователя """
    id: int
    created_at: datetime.datetime
    login: EmailStr
    project_id: int
    env: str
    domain: str
    locktime: datetime.datetime | None

    model_config = ConfigDict(from_attributes=True)


class SUserId(BaseModel):
    """Тело ответа об создании пользователя"""
    ok: bool = True
    user_id: int


class SUserLockAdd(BaseModel):
    id: int


class SUserLockResp(SUserLockAdd):
    locked_yet: bool = False
    locktime: datetime.datetime | None


class ResponseError(BaseModel):
    error: bool
