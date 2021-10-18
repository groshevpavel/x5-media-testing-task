import typing as t

from pydantic import BaseModel


class User(BaseModel):
    firstname: str
    lastname: str


class UserId(BaseModel):
    id: int


class UserAdd(User):
    bonus_points: t.Optional[int] = 0


class UserAdded(UserAdd, UserId):
    pass
