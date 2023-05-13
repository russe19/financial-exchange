from fastapi import HTTPException
from pydantic import BaseModel, validator


class CurrencyCreate(BaseModel):
    name: str
    course: str

    @validator('course')
    def course_validation_create(cls, value):
        if value[-1:-3:-1].isnumeric() and value[-3] == '.' and value[-4::-1].isnumeric():
            return value.title()
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": str("Неправильно веден формат валюты, требуется число с 2-мя знаками после точки"),
            "details": None
        })


class CurrencyUpdate(BaseModel):
    course: str

    @validator('course')
    def course_validation_update(cls, value):
        if value[-1:-3:-1].isnumeric() and value[-3] == '.' and value[-4::-1].isnumeric():
            return value.title()
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": str("Неправильно веден формат валюты, требуется число с 2-мя знаками после точки"),
            "details": None
        })


class UserCurrencyCreateModel(BaseModel):
    count: str

    @validator('count')
    def count_validate_user(cls, value):
        if value[-1:-3:-1].isnumeric() and value[-3] == '.' and value[-4::-1].isnumeric():
            return value.title()
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": str("Неправильно веден формат количества средств, требуется число с 2-мя знаками после точки"),
            "details": None
        })

