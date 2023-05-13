import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from operations.models import Operation
from operations.schemas import OperationCreate, BalanceUp
from operations.service import operation_data, currency_data, user_data
from auth.base_config import current_user
from currency.models import Currency, UserCurrency
# from tasks.tasks import buy_or_sell, balance_transaction
from auth.models import Role, User


router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)


# @router.get("/long_operation")
# @cache(expire=30)
# def get_long_op():
#     time.sleep(2)
#     return "Данные"


@router.get("/operations")
async def get_operations(limit: int = 5, offset: int = 0, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Operation).offset(offset).limit(limit)
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


@router.post("/operations")
async def new_currency(new_operation: OperationCreate, username=Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        currency_id = new_operation.dict().get("currency")
        count = new_operation.dict().get("count")
        summ = round(float(new_operation.dict().get("count")) * float(new_operation.dict().get("cost")), 2)
        if float(username.balance) < summ:
            raise ValueError("У вас недостаточно средств для оформления операции")
        else:
            curr = insert(Operation).values(status="active", username1=username.id,
                                            creation_at=datetime.datetime.utcnow(), **new_operation.dict())
            await session.execute(curr)
            if new_operation.dict().get("side") == "buy":
                #Пользователь получает валюту
                search = select(UserCurrency).where(UserCurrency.username == username.id).where(
                    UserCurrency.curr == currency_id)
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
            elif new_operation.dict().get("side") == "sell":
                # Пользователь отдает валюту
                search = select(UserCurrency).where(UserCurrency.username == username.id).where(
                    UserCurrency.curr == currency_id)
                result = await session.execute(search)
                if result.all() == []:
                    raise ValueError('Пользователь не владеет данной валютой ')
                else:
                    search = select(UserCurrency).where(UserCurrency.username == username.id).where(
                        UserCurrency.curr == currency_id)
                    search_result = await session.execute(search)
                    old_count = float(search_result.first().UserCurrency.__dict__['count'])
                    if old_count < float(count):
                        raise ValueError('Пользователь не обладает валютой в должном размере')
                    new_count = str(round(old_count - float(count), 2))
                    up_us_cur = update(UserCurrency).filter(UserCurrency.username == username.id).filter(
                        UserCurrency.curr == currency_id).values(count=new_count)
                    await session.execute(up_us_cur)
            else:
                raise ValueError("Неверная операция")

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


@router.get("/oper_type")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Operation).where(Operation.side == operation_type)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.all(),
            "details": None
        }
    except Exception:
        # Передать ошибку разработчикам
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.post("/buy/{operation_id}")
async def user_buy_or_sell(operation_id: int, username=Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        # Получение информации об операции
        operation = await session.execute(select(Operation).filter(Operation.id == operation_id))
        operation_dict, side, status, count, currency_id, user_first_id, cost_set_user = operation_data(operation)

        # Получение информации об валюте
        currency = await session.execute(select(Currency).filter(Currency.id == currency_id))
        currency_dict, currency_id, currency_name, currency_course = currency_data(currency)
        cost = round((float(count) * float(cost_set_user)), 2)

        # Получение информации о пользователях учавствующих в транзакции
        user_first = await session.execute(select(User).filter(User.id == user_first_id))
        user_first_dict, user_second_dict, u_first_balance, \
            u_first_id, u_second_balance, u_second_id = user_data(user_first, username)

        # Если операция buy, то авторизированный пользователь совершает покупку и у него списываются средства
        if side == "buy" and status == "active" and u_second_balance >= cost and u_first_id != u_second_id:
            # Операция становится неактивной
            mod_operation = update(Operation).where(Operation.id == operation_id).values(
                status='inactive',
                username2=user_second_dict.get("id"),
            )
            await session.execute(mod_operation)
            # Баланс первого пользователя увеличился
            user_first_balance = update(User).where(User.id == operation_dict.get("username1")).values(
                balance=str(round(float(user_first_dict.get("balance")), 2) + cost)
            )
            await session.execute(user_first_balance)
            # Баланс второго пользователя уменьшился
            user_second_balance = update(User).where(User.id == user_second_dict.get("id")).values(
                balance=str(round(float(user_second_dict.get("balance")), 2) - cost)
            )
            await session.execute(user_second_balance)
            # Второго пользователь получил валюту
            search = select(UserCurrency).where(UserCurrency.username == u_second_id).where(UserCurrency.curr == currency_id)
            result = await session.execute(search)
            if result.all() == []:
                await session.execute(insert(UserCurrency).values(username=u_second_id, curr=currency_id, count=count))
            else:
                search = select(UserCurrency).where(UserCurrency.username == u_second_id).where(
                    UserCurrency.curr == currency_id)
                search_result = await session.execute(search)
                old_count = float(search_result.first().UserCurrency.__dict__['count'])
                new_count = str(round(float(count) + old_count, 2))
                up_us_cur = update(UserCurrency).filter(UserCurrency.username == u_second_id).filter(
                    UserCurrency.curr == currency_id).values(username=u_second_id, curr=currency_id, count=new_count)
                await session.execute(up_us_cur)
        # Если операция sell, то авторизированный пользователь совершает продажу и у него пополняются денежные средства
        elif side == "sell" and status == "active" and u_first_balance >= cost and u_first_id != u_second_id:
            # Операция становится неактивной
            mod_operation = update(Operation).where(Operation.id == operation_id).values(
                status='inactive',
                username2=user_second_dict.get("id"),
            )
            await session.execute(mod_operation)
            # Баланс первого пользователя уменьшился
            user_first_balance = update(User).where(User.id == operation_dict.get("username1")).values(
                balance=str(round(float(user_first_dict.get("balance")), 2) - cost)
            )
            await session.execute(user_first_balance)
            # Баланс второго пользователя увеличился
            user_second_balance = update(User).where(User.id == user_second_dict.get("id")).values(
                balance=str(round(float(user_second_dict.get("balance")), 2) + cost)
            )
            await session.execute(user_second_balance)
            # Второй пользователь отдает валюту
            search = select(UserCurrency).where(UserCurrency.username == u_second_id).where(
                UserCurrency.curr == currency_id)
            result = await session.execute(search)
            if result.all() == []:
                raise ValueError('Пользователь не владеет данной валютой ')
            else:
                search = select(UserCurrency).where(UserCurrency.username == u_second_id).where(
                    UserCurrency.curr == currency_id)
                search_result = await session.execute(search)
                old_count = float(search_result.first().UserCurrency.__dict__['count'])
                if old_count < float(count):
                    raise ValueError('Пользователь не обладает валютой в должном размере')
                new_count = str(round(old_count - float(count), 2))
                up_us_cur = update(UserCurrency).filter(UserCurrency.username == u_second_id).filter(
                    UserCurrency.curr == currency_id).values(username=u_second_id, curr=currency_id, count=new_count)
                await session.execute(up_us_cur)
        else:
            if u_first_id == u_second_id:
                raise ValueError('Пользователь не может совершить покупку у себя')
            elif status != "active":
                raise ValueError('Данная операция не является активной')
            elif u_first_balance < cost and side == "sell" or u_second_balance < cost and side == "buy":
                raise ValueError('Пользователь не может совершить покупку, поскольку у него недостаточно средств')
            elif side == "sell" or side == "buy":
                raise ValueError('Неверный тип операции')
            else:
                raise ValueError('Неизвестная ошибка')
        await session.commit()
        return {
            "status": 'success',
            "data": {'side': u_first_balance, 'status': u_second_balance, 'user': user_second_dict.get("balance")},
            "details": None
        }
    except Exception as e:
        # Передать ошибку разработчикам
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": str(e),
            "details": None
        })


@router.put("/up_balance/{count}")
async def user_buy_or_sell(up_balance: BalanceUp, username=Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        user = await session.execute(select(User).where(User.id == username.id))
        new_balance = str(float(username.balance) + float(up_balance.dict().get("count")))
        balance = update(User).where(User.id == username.id).values(balance=new_balance)
        await session.execute(balance)
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": str(e),
            "details": None
        })


@router.get("/my_balance")
async def user_buy_or_sell(username=Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    my_balance = username.balance
    return {
        "status": 'success',
        "data": {'balance': my_balance},
        "details": None
    }


@router.get("/my_profile")
async def user_profile(username=Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    user = await session.execute(select(User).where(User.id == username.id))
    return {
        "status": 'success',
        "data": {'balance': user.first()},
        "details": None
    }
