# from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy import insert, select, update, delete, create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from database import DATABASE_URL
#
# from celery import Celery
# from starlette.responses import JSONResponse
#
# from database import get_async_session
# from config import SMTP_PASSWORD, SMTP_USER, REDIS_HOST, REDIS_PORT
# from operations.models import Operation
# from currency.models import Currency
# from auth.base_config import current_user
# from auth.models import User, Role
# from typing import AsyncGenerator
#
#
# celery = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')
#
#
# engine = create_engine(DATABASE_URL, pool_pre_ping=True)
# async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
#
#
# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session_maker() as session:
#         yield session
#
#
#
# @celery.task
# def buy_or_sell(operation: int, username: id):
#     session = Depends(get_async_session)
#     # with open('text.txt', 'w', encoding='utf-8') as f:
#     #     f.write(str(session))
#     curr = delete(Role).where(id=1)
#     session.execute(curr)
#     # price = float(Operation.count) * float(session.execute(curr).course)
#     # operate = update(Operation).where(Operation.id == operation).values(username2=username, status='inactive')
#     # await session.execute(operate)
#     # operate = select(Operation).where(Operation.id == operation)
#     # oper_user = session.execute(operate)
#     # user_1 = update(User).where(User.id == oper_user.username1).values(balance)
#     #
#     # us_1 = update(User).where(Operation.id == operation).values(username2=username, status='inactive')
#     session.commit()
#     # return ss.all()
#
#
# @celery.task
# def balance_transaction(count: str, username: id, session=Depends(get_async_session)):
#     user = session.execute(select(User).where(User.id == username.id))
#     balance_user = user.first()["User"].balance
#     new_balance = str(float(balance_user) + float(count))
#     balance = update(User).where(User.id == username.id).values(balance=new_balance)
#     session.execute(balance)
#     session.commit()
