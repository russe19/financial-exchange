from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from auth.base_config import current_user
from auth.models import User

from database import get_async_session
from currency.models import Currency, UserCurrency
from currency.schemas import CurrencyCreate, CurrencyUpdate, UserCurrencyCreateModel

router = APIRouter(
    prefix="/Currencies",
    tags=["Currencies"]
)


@router.get("/currency")
async def get_currencies(limit: int = 5, offset: int = 0, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Currency).offset(offset).limit(limit)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.all(),
            "details": None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": str(e),
            "details": None
        })


@router.post("/currency")
async def new_currency(new_currency: CurrencyCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        curr = insert(Currency).values(**new_currency.dict())
        await session.execute(curr)
        await session.commit()
        return {
            "status": "success",
            "data": "Данные успешно созданы",
            "details": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": str(e),
            "details": None
        })


@router.put("/currency/{item}")
async def update_currency(update_currency: CurrencyUpdate, item: str, session: AsyncSession = Depends(get_async_session)):
    try:
        curr = update(Currency).where(Currency.name == item).values(**update_currency.dict())
        await session.execute(curr)
        await session.commit()
        return {
            "status": "success",
            "data": "Данные успешно обновлены",
            "details": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": str(e),
            "details": None
        })


@router.delete("/currency/{item}")
async def update_currency(item: str, session: AsyncSession = Depends(get_async_session)):
    try:
        curr = delete(Currency).where(Currency.name == item)
        await session.execute(curr)
        await session.commit()
        return {
            "status": "success",
            "data": "Данные успешно удалены",
            "details": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": str(e),
            "details": None
        })


@router.put("/buy_currency/{cur_id}")
async def new_user_currency(cur_id: int, user_cur: UserCurrencyCreateModel, username=Depends(current_user),
                            session: AsyncSession = Depends(get_async_session)):
    try:
        search = select(UserCurrency).where(UserCurrency.username == username.id).where(UserCurrency.curr == cur_id)
        result = await session.execute(search)
        if result.all() == []:
            await session.execute(insert(UserCurrency).values(username=username.id, curr=cur_id, **user_cur.dict()))
        else:
            search = select(UserCurrency).where(UserCurrency.username == username.id).where(UserCurrency.curr == cur_id)
            search_result = await session.execute(search)
            old_count = float(search_result.first().UserCurrency.__dict__['count'])
            new_count = str(round(float(user_cur.dict().get('count')) + old_count, 2))
            up_us_cur = update(UserCurrency).filter(UserCurrency.username == username.id).\
                filter(UserCurrency.curr == cur_id).values(username=username.id, curr=cur_id, count=new_count)
            await session.execute(up_us_cur)
        await session.commit()
        return {
            "status": "success",
            "data": f"Баланс валюты успешно обновлен, в кошельке {new_count} единиц",
            "details": None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": str(e),
            "details": None
        })


@router.post("/buy_currency/{currency_id}")
async def user_buy_currency(currency_id: int, buy_currency: UserCurrencyCreateModel, username=Depends(current_user),
                            session: AsyncSession = Depends(get_async_session)):
    try:
        count = buy_currency.dict().get("count")
        currency = await session.execute(select(Currency).where(Currency.id == currency_id))
        currency_course = float(currency.first().Currency.__dict__['course'])
        summ = 1.1 * (float(count) * currency_course)
        if summ > float(username.balance):
            raise ValueError("Недостаточно средств")
        else:
            await session.execute(update(User).filter(User.id == username.id).
                                  values(balance=str(round(float(username.balance) - summ, 2))))
            search = select(UserCurrency).where(UserCurrency.username == username.id).\
                where(UserCurrency.curr == currency_id)
            result = await session.execute(search)
            if result.all() == []:
                await session.execute(
                    insert(UserCurrency).values(username=username.id, curr=currency_id, count=count)
                )
            else:
                search = select(UserCurrency).where(UserCurrency.username == username.id).where(
                    UserCurrency.curr == currency_id)
                search_result = await session.execute(search)
                old_count = float(search_result.first().UserCurrency.__dict__['count'])
                new_count = str(round(float(count) + old_count, 2))
                up_us_cur = update(UserCurrency).filter(UserCurrency.username == username.id).filter(
                    UserCurrency.curr == currency_id).values(count=new_count)
                await session.execute(up_us_cur)
            await session.commit()
        return {
            "status": "success",
            "data": "Валюта успешно приобретена",
            "details": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": str(e),
            "details": None
        })


