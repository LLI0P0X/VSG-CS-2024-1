from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import insert, update, select, delete
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column

import asyncio
import datetime
import os

import config


DATABASE_URL = config.DB_URL
engine = create_async_engine(
    url=DATABASE_URL,
    echo=False,
)

class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'
    uid: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    passHash: Mapped[str]
