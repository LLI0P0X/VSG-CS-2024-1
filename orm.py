from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import insert, update, select, delete
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column

import asyncio
import datetime
import os

engine = create_async_engine(
    url=f"sqlite+aiosqlite:///{os.path.join(os.path.dirname(__file__), 'db.session')}",
    echo=False,
)


class Base(DeclarativeBase):
    pass


class Reports(Base):
    __tablename__ = 'reports'
    rid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ip: Mapped[str]
    protocol: Mapped[str]
    port: Mapped[int]
    cve: Mapped[str]
    hazard: Mapped[str]
    link: Mapped[str]


class Tasks(Base):
    __tablename__ = 'tasks'
    tid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fromIp: Mapped[str]
    toIp: Mapped[str]
    ready: Mapped[bool]
    nextRun: Mapped[datetime.datetime | None]
    cycle: Mapped[datetime.timedelta | None]
    email: Mapped[str | None]
    rid: Mapped[int | None] = mapped_column(ForeignKey('Reports.rid'), ondelete='CASCADE')


async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def remove_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def add_task(fromIp, toIp, nextRun, cycle, email):
    async with engine.begin() as conn:
        await conn.execute(
            insert(Tasks).values(fromIp=fromIp, toIp=toIp, ready=False, nextRun=nextRun, cycle=cycle, email=email,
                                 rid=None)
        )


async def remove_task(tid):
    async with engine.begin() as conn:
        await conn.execute(
            delete(Tasks).where(Tasks.tid == tid)
        )


async def complete_task(tid):
    async with engine.begin() as conn:
        await conn.execute(
            update(Tasks).where(Tasks.tid == tid).values(ready=True)
        )


async def add_report(ip, protocol, port, cve, hazard, link):
    async with engine.begin() as conn:
        await conn.execute(
            insert(Reports).values(ip=ip, protocol=protocol, port=port, cve=cve, hazard=hazard, link=link)
        )


async def main():
    await remove_all()
    await create_all()
    await add_task('127.0.0.1', '127.0.0.2', datetime.datetime.now(), datetime.timedelta(days=1), 'test@mail.com')


if __name__ == '__main__':
    asyncio.run(main())
