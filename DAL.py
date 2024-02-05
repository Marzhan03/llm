from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import databases
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from databases import Database
from sqlalchemy.orm import sessionmaker
import dotenv, os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine



dotenv.load_dotenv(override=True)
DATABASE_URL = os.getenv("DATABASE_URL")
print("DSfsdfsd", DATABASE_URL)
async_engine = create_async_engine(DATABASE_URL, echo=True)
database = Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()


# Base.metadata.create_all(bind=async_engine)

# Создаем сессию для взаимодействия с базой данных
# SessionLocal = sessionmaker(async_engine,class_ = AsyncSession, autocommit=False, autoflush=False)
# session = SessionLocal
# news = sqlalchemy.Table(
#     "news",
#     metadata,
#     Column("id", Integer, primary_key=True, index=True),
#     Column("title", String, index=True),
#     Column("date", DateTime),
#     Column("content", String),
#     Column("category_id", Integer),
#     Column("location_id", Integer),
#     Column("site_id", Integer),
#     Column("old_id", Integer),
#     Column("summarized_content", String)
# )

async_session = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
