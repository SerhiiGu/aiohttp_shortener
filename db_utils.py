import asyncio
import os
import warnings

from aiopg.sa import create_engine
import sqlalchemy as sa
from sqlalchemy.schema import CreateTable


warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=ResourceWarning)

metadata = sa.MetaData()
tbl = sa.Table(
    'links', metadata,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('new_link', sa.String(255)),
    sa.Column('old_link', sa.String(255)),
    sa.Column('user', sa.String(255), nullable=True)
)


async def connect_db():
    engine = await create_engine(user='postgres',
                                 password='qwe123',
                                 host=os.getenv('DB_HOST', '127.0.0.1'),
                                 port=5432,
                                 database='postgres')
    return engine


async def create_table():
    engine = await connect_db()
    async with engine.acquire() as conn:
        create_tbl = CreateTable(tbl)
        await conn.execute(create_tbl)


async def insert_data(old_link, new_link, user=None):
    engine = await connect_db()
    async with engine.acquire() as conn:
        await conn.execute(tbl.insert().values(old_link=old_link, new_link=new_link, user=user))


async def get_link(new_link):
    engine = await connect_db()
    async with engine.acquire() as conn:
        result = await conn.execute(tbl.select().where(tbl.c.new_link == new_link))
        result = await result.fetchone()
        return result


async def get_user_links(user_id):
    engine = await connect_db()
    async with engine.acquire() as conn:
        results = await conn.execute(tbl.select().where(tbl.c.user == str(user_id)))
        results = await results.fetchall()
        links = [f"http://127.0.0.1:8080/{result[1]} -> {result[2]}" for result in results]
        return links
