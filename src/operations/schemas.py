from datetime import datetime

from fastapi import HTTPException
from pydantic import BaseModel, validator


class OperationCreate(BaseModel):
    side: str
    count: str
    currency: int
    cost: str

    @validator("side")
    def validation_course_create(cls, value):
        if value == "buy" or value == "sell":
            return value
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": str("Введен недопустимый тип операции"),
            "details": None
        })

    @validator('count')
    def validation_count_create(cls, value):
        if value[-1:-3:-1].isnumeric() and value[-3] == '.' and value[-4::-1].isnumeric():
            return value
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": str("Неправильно веден формат данных, требуется число с 2-мя знаками после точки"),
            "details": None
        })

    @validator("cost")
    def validate_cost(cls, value):
        if value[-1:-3:-1].isnumeric() and value[-3] == '.' and value[-4::-1].isnumeric():
            return value
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": str("Неправильно введен формат установленной цены, требуется число с 2-мя знаками после точки"),
            "details": None
        })


class BalanceUp(BaseModel):
    count: str

    @validator('count')
    def validation_count_create(cls, value):
        if value[-1:-3:-1].isnumeric() and value[-3] == '.' and value[-4::-1].isnumeric():
            return value
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": str("Неправильно ведена сумма для пополнения баланса, требуется число с 2-мя знаками после точки"),
            "details": None
        })
