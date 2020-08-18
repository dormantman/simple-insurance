import datetime
from functools import reduce
from typing import List

from fastapi import APIRouter, HTTPException

import schemas
from models import (
    InsuranceRate, InsuranceRatePydantic, User,
    UserInPydantic,
    UserPydantic,
    UserPydanticList,
)
from utils import template_for_404

router = APIRouter()


@router.get('/rates/', response_model=List[InsuranceRatePydantic])
async def get_rates():
    return await InsuranceRatePydantic.from_queryset(InsuranceRate.all().order_by('-created').limit(50))


@router.post('/rates/', response_model=schemas.RateUploadAnswer)
async def upload_rates(rate_data: dict):
    uploaded = False

    print(rate_data)

    insurance_rates = reduce(lambda first, second: first + second, [
        [dict(date=date, **element) for element in rate_data[date]]
        for date in rate_data if date
    ])

    for insurance_rate in insurance_rates:
        cargo_type, rate = insurance_rate.get('cargo_type'), insurance_rate.get('rate')
        created = datetime.datetime.strptime(insurance_rate.get('date'), '%Y-%m-%d')
        rate_data = dict(cargo_type=cargo_type, rate=rate, created=created)

        similar_rates = await InsuranceRate.filter(**rate_data)
        if not similar_rates:
            uploaded = True

    return schemas.RateUploadAnswer(
        message='Rate was uploaded successfully' if uploaded else 'All changes have already been uploaded',
        status=uploaded,
    )


@router.get('/price/', response_model=schemas.InsurancePrice)
async def get_price(cost: float, cargo_type: str, date: datetime.datetime):
    queryset = InsuranceRate.filter(cargo_type=cargo_type, created__lte=date).order_by('created')
    data = await queryset.first()
    if not data:
        return
    return schemas.InsurancePrice(price=cost * data.rate, rate=data.rate, date=data.created)


@router.post('/')
async def get_schemas():
    print(f"{UserPydantic.schema()}\n{'*' * 20}")
    user = await User.create(email="e@e.com", hashed_password="123456", is_active=True)
    user_schema = await UserInPydantic.from_tortoise_orm(user)
    print(user_schema.json())
    return user_schema.json()


@router.post('/test_create')
async def create_users():
    await User.create(email="e4@e.com", hashed_password="123456", is_active=True)
    await User.create(email="e2@e.com", hashed_password="123456", is_active=False)
    await User.create(email="e3@e.com", hashed_password="123456", is_active=True)
    user_schema = await UserPydanticList.from_queryset(User.all())
    print(user_schema.dict())
    print(user_schema.json())
    return user_schema.json()


@router.get("/", response_model=UserPydantic)
async def get_users_list():
    data = await InsuranceRatePydantic.from_queryset_single(InsuranceRate.get(id=1))
    print(data.json())
    users = await UserPydantic.from_queryset_single(User.get(id=3))
    print(users.json())
    return users


@router.get("/users", response_model=List[UserPydantic])
async def get_users():
    return await UserPydantic.from_queryset(User.all())


@router.post("/users", response_model=UserPydantic)
async def create_user(user: UserInPydantic):
    user_obj = await User.create(**user.dict(exclude_unset=True))
    return await UserPydantic.from_tortoise_orm(user_obj)


@router.get("/user/{user_id}", response_model=UserPydantic, **template_for_404())
async def get_user(user_id: int):
    return await UserPydantic.from_queryset_single(User.get(id=user_id))


@router.post("/user/{user_id}", response_model=UserPydantic, **template_for_404())
async def update_user(user_id: int, user: UserInPydantic):
    await User.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return await UserPydantic.from_queryset_single(User.get(id=user_id))


@router.delete("/user/{user_id}", response_model=schemas.Status, **template_for_404())
async def delete_user(user_id: int):
    deleted_count = await User.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return schemas.Status(message=f"Deleted user {user_id}")
