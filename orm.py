import sqlalchemy.engine.cursor
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
    tid: Mapped[int]
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
    ports: Mapped[str | None]
    ready: Mapped[bool]
    nextRun: Mapped[datetime.datetime | None]
    cycle: Mapped[datetime.timedelta | None]
    email: Mapped[str | None]


async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def remove_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def add_task(fromIp, toIp, ports, nextRun, cycle, email):
    async with engine.begin() as conn:
        result = await conn.execute(
            insert(Tasks).values(fromIp=fromIp, toIp=toIp, ports=ports, ready=False, nextRun=nextRun, cycle=cycle,
                                 email=email)
        )
        return result.inserted_primary_key[0]


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


async def get_ready_from_task(tid):
    async with engine.begin() as conn:
        result = await conn.execute(
            select(Tasks).where(Tasks.tid == tid)
        )
        return result.first().ready


async def get_task(tid):
    async with engine.begin() as conn:
        result = await conn.execute(
            select(Tasks).where(Tasks.tid == tid)
        )
        return result.first()


async def update_task(tid, fromIp, toIp, ready, nextRun, cycle, email):
    async with engine.begin() as conn:
        await conn.execute(
            update(Tasks).where(Tasks.tid == tid).values(fromIp=fromIp, toIp=toIp, ready=ready, nextRun=nextRun,
                                                         cycle=cycle, email=email)
        )


async def get_tasks_by_need_run():
    async with engine.begin() as conn:
        result = await conn.execute(
            select(Tasks).where(Tasks.ready == False, Tasks.nextRun < datetime.datetime.now())
            .order_by(Tasks.nextRun).limit(1)
        )
        return result.first()


async def add_report(tid, ip, protocol, port, cve, hazard, link):
    async with engine.begin() as conn:
        await conn.execute(
            insert(Reports).values(tid=tid, ip=ip, protocol=protocol, port=port, cve=cve, hazard=hazard, link=link)
        )


async def get_reports_by_tid(tid):
    async with engine.begin() as conn:
        result = await conn.execute(
            select(Reports).where(Reports.tid == tid)
        )
        return result.fetchall()


async def select_tasks():
    async with engine.begin() as conn:
        result = await conn.execute(
            select(Tasks)
        )
        return result.fetchall()


async def select_reports():
    async with engine.begin() as conn:
        result = await conn.execute(
            select(Reports)
        )
        return result.fetchall()


async def main():
    await remove_all()
    await create_all()
    a1 = await add_task('138.201.80.190', '138.201.80.190', datetime.datetime.now() + datetime.timedelta(minutes=-1),
                        datetime.timedelta(days=1), 'test@mail.com')
    a2 = await add_task('127.0.0.1', '127.0.0.2', datetime.datetime.now() + datetime.timedelta(minutes=-1),
                        datetime.timedelta(days=1), 'test@mail.com')
    a3 = await add_task('127.0.0.1', '127.0.0.2', datetime.datetime.now() + datetime.timedelta(minutes=-1),
                        datetime.timedelta(days=1), 'test@mail.com')
    print(a1, a2, a3)
    print(await get_ready_from_task(a2))
    print(await select_tasks())
    print(await select_reports())
    # print(await get_tasks_by_need_run())


if __name__ == '__main__':
    asyncio.run(main())
