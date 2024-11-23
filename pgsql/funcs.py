from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import insert, update, select, delete
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column

import asyncio
import datetime
import os

import config

import tables
from tables import engine, Users


async def add_user(email, passHash):
    async with engine.begin() as conn:
        await conn.execute(
            insert(Users).values(email=email, passHash=passHash)
        )


async def select_users():
    async with engine.begin() as conn:
        result = await conn.execute(select(Users))
        return result.fetchall()


async def main():
    print(await select_users())


if __name__ == "__main__":
    asyncio.run(main())
