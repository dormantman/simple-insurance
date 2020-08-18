import datetime

from pydantic import BaseModel
from tortoise.contrib.pydantic.base import PydanticModel


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
