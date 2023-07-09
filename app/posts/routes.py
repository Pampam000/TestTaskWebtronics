from fastapi import Depends, APIRouter, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import auth
from app.db import get_db
from app.users import models as user_models
from . import crud, models
from .schemas import BasePost, Post

router = APIRouter(prefix='/posts', tags=["posts"])


@router.get("/", response_model=list[Post])
async def get_posts(
        session: AsyncSession = Depends(get_db),
        offset: int = Query(None, ge=1),
        limit: int = Query(None, ge=1)):
    result: list[models.Post] = await crud.get_posts(session=session,
                                                     offset=offset,
                                                     limit=limit)
    return result


@router.post('/', response_model=Post)
async def create_post(post: BasePost,
                      session: AsyncSession = Depends(get_db),
                      current_user: user_models.User = Depends(
                          auth.get_current_user)):
    data = post.dict() | {'user_id': current_user.id}
    created_post: models.Post = await crud.create_post(session=session,
                                                       data=data)

    return created_post


@router.put('/{post_id}', response_model=Post)
async def update_post(post: BasePost,
                      post_id: int = Path(ge=1),
                      session: AsyncSession = Depends(get_db),
                      current_user: user_models.User = Depends(
                          auth.get_current_user)):
    return await crud.update_post(session=session,
                                  post_id=post_id,
                                  data=post.dict(exclude={'id'}),
                                  user_id=current_user.id)


@router.delete('/{post_id}', response_model=Post)
async def delete_post(post_id: int = Path(ge=1),
                      session: AsyncSession = Depends(get_db),
                      current_user: user_models.User = Depends(
                          auth.get_current_user)):
    return await crud.delete_post(session=session,
                                  post_id=post_id,
                                  user_id=current_user.id)
