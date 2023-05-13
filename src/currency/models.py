from sqlalchemy.orm import validates
from sqlalchemy import Column, ForeignKey, Integer, String

from database import Base


class Currency(Base):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    course = Column(String, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @validates("course")
    def validate_course(self, key, value):
        if value[-1:-3:-1].isnumeric() and value[-3] == '.' and value[-4::-1].isnumeric():
            return value
        raise ValueError("Неправильно веден формат валюты, требуется число с 2-мя знаками после точки")


class UserCurrency(Base):
    __tablename__ = "user_currency"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Integer, ForeignKey("user.id"), nullable=False)
    curr = Column(Integer, ForeignKey("currency.id"), nullable=False)
    count = Column(String, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @validates("count")
    def validate_user_currency(self, key, value):
        if value[-1:-3:-1].isnumeric() and value[-3] == '.' and value[-4::-1].isnumeric():
            return value
        raise ValueError("Неправильно веден формат количества, требуется число с 2-мя знаками после точки")
