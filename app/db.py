from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, \
    AsyncEngine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import DATABASE_URL

Base = declarative_base()
engine: AsyncEngine = create_async_engine(DATABASE_URL)

async_session = sessionmaker(engine,
                             expire_on_commit=False,
                             class_=AsyncSession)


async def get_db():
    async with async_session() as session:
        yield session

