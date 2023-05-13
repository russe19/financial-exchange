from sqlalchemy import TIMESTAMP, Column, Integer, MetaData, String, Table, ForeignKey, Boolean
from sqlalchemy.orm import validates
from datetime import datetime
from database import Base


class Operation(Base):
    __tablename__ = "operation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username1 = Column(Integer, ForeignKey("user.id"), nullable=False)
    username2 = Column(Integer, ForeignKey("user.id"))
    status = Column(String, nullable=False)
    side = Column(String, nullable=False)
    creation_at = Column(TIMESTAMP, default=datetime.utcnow)
    currency = Column(Integer, ForeignKey("currency.id"), nullable=False)
    cost = Column(String, nullable=False)
    count = Column(String, nullable=False)

    @validates("status")
    def validate_course(self, key, value):
        if value == "active" or value == "inactive":
            return value
        raise ValueError("Введен недопустимый статус")

    @validates("side")
    def validate_course(self, key, value):
        if value == "buy" or value == "sell":
            return value
        raise ValueError("Введен недопустимый тип операции")

    @validates("count")
    def validate_course(self, key, value):
        if value[-1:-3:-1].isnumeric() and value[-3] == '.' and value[-4::-1].isnumeric():
            return value
        raise ValueError("Неправильно введен формат данных, требуется число с 2-мя знаками после точки")

    @validates("cost")
    def validate_cost(self, key, value):
        if value[-1:-3:-1].isnumeric() and value[-3] == '.' and value[-4::-1].isnumeric():
            return value
        raise ValueError("Неправильно введен формат установленной цены, требуется число с 2-мя знаками после точки")
