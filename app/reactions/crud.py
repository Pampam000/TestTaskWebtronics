from fastapi import HTTPException, status
from sqlalchemy import insert, update, delete
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Insert, Update, Delete

from app.error_mesages import NOT_FOUND, IS_OWNER
from app.posts import crud as posts_crud
from app.posts.models import Post
from app.reactions.models import UserPostReaction


async def create_user_post_reaction(session: AsyncSession,
                                    data: dict) -> UserPostReaction:
    query: Insert = insert(UserPostReaction).values(data) \
        .returning(UserPostReaction)
    result: CursorResult = await session.execute(query)
    result: UserPostReaction = result.fetchone()
    await session.commit()
    return result


async def update_user_post_reaction(session: AsyncSession,
                                    post_id: int,
                                    user_id: int,
                                    data: dict) -> UserPostReaction:
    query: Update = update(UserPostReaction) \
        .where(UserPostReaction.post_id == post_id) \
        .where(UserPostReaction.user_id == user_id) \
        .values(data).returning(UserPostReaction)
    result: CursorResult = await session.execute(query)
    result: UserPostReaction = result.fetchone()
    await session.commit()
    return result


async def delete_user_post_reaction(session: AsyncSession,
                                    post_id: int,
                                    user_id: int) -> UserPostReaction:
    query: Delete = delete(UserPostReaction) \
        .where(UserPostReaction.post_id == post_id) \
        .where(UserPostReaction.user_id == user_id) \
        .returning(UserPostReaction)
    result: CursorResult = await session.execute(query)
    result: UserPostReaction = result.fetchone()
    await session.commit()
    return result


async def set_user_post_reaction(session: AsyncSession,
                                 post_id: int,
                                 user_id: int,
                                 reaction_value: str) -> UserPostReaction:
    post: Post | None = await posts_crud.get_post_by_id(session=session,
                                                        post_id=post_id,
                                                        prefetch_related=True)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=NOT_FOUND.format(instance='Post',
                                                    id=post_id))
    if post.user_id == user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=IS_OWNER.format(
                                user_id=user_id,
                                instance='Post',
                                action='make reaction on',
                                instance_id=post_id))

    user_ids = [r.user_id for r in post.reactions]
    if user_id not in user_ids:
        data = {
            'user_id': user_id,
            'post_id': post_id,
            'reaction_value': reaction_value
        }
        return await create_user_post_reaction(session=session, data=data)
    else:
        index: int = user_ids.index(user_id)
        user_post_reaction: UserPostReaction = post.reactions[index]

        if user_post_reaction.reaction_value != reaction_value:
            data = {'reaction_value': reaction_value}
            return await update_user_post_reaction(session=session,
                                                   post_id=post_id,
                                                   user_id=user_id,
                                                   data=data)
        else:
            return await delete_user_post_reaction(session=session,
                                                   post_id=post_id,
                                                   user_id=user_id)
