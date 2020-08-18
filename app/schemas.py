import datetime
from typing import List

from pydantic import BaseModel
from tortoise.contrib.pydantic.base import PydanticModel


class ItemBase(PydanticModel):
    title: str
    description: str = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner: int

    class Config:
        orm_mode = True


class UserBase(PydanticModel):
    email: str


class UserCreate(UserBase):
    password: str
    is_active: bool = True

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    id: int


class User(UserBase):
    id: int
    items: List[Item] = []

    class Config:
        orm_mode = True


class ItemUser(ItemBase):
    id: int
    owner: UserInDB


class Status(BaseModel):
    message: str


class InsuranceRateBase(PydanticModel):
    cargo_type: str = None
    rate: float = None


class InsuranceRateCreate(InsuranceRateBase):
    cargo_type: str
    rate: float
    created: datetime.datetime

    class Config:
        orm_mode = True


class InsuranceRate(InsuranceRateBase):
    id: int
    created: datetime.datetime

    class Config:
        orm_mode = True


class InsurancePrice(BaseModel):
    price: float
    rate: float
    date: datetime.datetime

    class Config:
        orm_mode = True


class RateUploadAnswer(BaseModel):
    message: str
    status: bool
