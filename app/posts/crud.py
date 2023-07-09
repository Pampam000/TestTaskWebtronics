from fastapi import HTTPException, status
from sqlalchemy import select, insert, update
from sqlalchemy.engine import ChunkedIteratorResult, CursorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import Select, Insert, Update

from app.error_mesages import NOT_FOUND, NOT_OWNER
from .models import Post


async def get_post_by_id(session: AsyncSession,
                         post_id: int,
                         prefetch_related: bool = False) -> Post:
    query: Select = select(Post).where(Post.id == post_id)
    if prefetch_related:
        query = query.options(joinedload(Post.reactions)
                              .load_only('user_id', 'reaction_value'))

    result: ChunkedIteratorResult = await session.execute(query)
    post: Post | None = result.scalar()
    return post


async def get_posts(session: AsyncSession,
                    offset: int = None,
                    limit: int = None) -> list[Post]:
    query: Select = select(Post).offset(offset).limit(limit).order_by(Post.id)
    query = query.options(
        joinedload(Post.reactions).load_only('user_id', 'reaction_value'))
    result: ChunkedIteratorResult = await session.execute(query)
    result = result.unique()
    result = result.scalars()
    return result.fetchall()


async def create_post(session: AsyncSession, data: dict) -> Post:
    query: Insert = insert(Post).values(data).returning(Post)
    result: CursorResult = await session.execute(query)
    result: Post = result.fetchone()
    await session.commit()
    return result


async def update_post(session: AsyncSession,
                      data: dict,
                      post_id: int,
                      user_id: int):
    post: Post | None = await get_post_by_id(session=session, post_id=post_id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=NOT_FOUND.format(instance='Post',
                                                    id=post_id))
    if post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=NOT_OWNER.format(
                                user_id=user_id,
                                instance='Post',
                                action='update',
                                instance_id=post_id))

    query: Update = update(Post).where(Post.id == post_id) \
        .values(data).returning(Post)

    result: CursorResult = await session.execute(query)
    result: Post = result.fetchone()
    await session.commit()
    return result


async def delete_post(session: AsyncSession, post_id: int, user_id: int):
    post: Post | None = await get_post_by_id(session=session, post_id=post_id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=NOT_FOUND.format(instance='Post',
                                                    id=post_id))

    if post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=NOT_OWNER.format(
                                user_id=user_id,
                                instance='Post',
                                action='delete',
                                instance_id=post_id))

    await session.delete(post)
    await session.commit()
    return post
