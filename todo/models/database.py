from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

with open("C:/Users/hrape/PycharmProjects/stepik_fastapi/todo/models/config.txt", "r") as config_file:
    SQLALCHEMY_DATABASE_URL = config_file.read().strip()

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL
)

AsyncSessionLocal = async_sessionmaker(engine, autocommit=False, autoflush=False, class_=AsyncSession)

Base = declarative_base()
