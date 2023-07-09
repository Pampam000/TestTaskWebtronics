from sqlalchemy import insert, select
from sqlalchemy.engine import CursorResult, ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Insert, Select

from .models import User


async def get_user_by_email(session: AsyncSession, email: str) -> User:
    query: Select = select(User).where(User.email == email)
    result: ChunkedIteratorResult = await session.execute(query)
    result: User = result.scalar()
    return result


async def create_user(session: AsyncSession, data: dict) -> User:
    query: Insert = insert(User).values(data).returning(User)
    result: CursorResult = await session.execute(query)
    result: User = result.fetchone()
    await session.commit()
    return result
