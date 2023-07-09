from fastapi import APIRouter, Query, Depends, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.auth import auth
from app.db import get_db
from app.users import models as user_models
from . import crud
from .schemas import Reaction, UserPostReaction

router = APIRouter(prefix='/posts/{post_id}/reaction',
                   tags=['reactions'])


@router.post('/', response_model=UserPostReaction)
async def create_user_post_reaction(
        reaction: str = Query(..., enum=[x.value for x in Reaction]),
        post_id: int = Path(..., ge=1),
        session: AsyncSession = Depends(get_db),
        current_user: user_models.User = Depends(
            auth.get_current_user)):
    if reaction not in [x.value for x in Reaction]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Reaction = ({reaction}) could not be set')

    return await crud.set_user_post_reaction(session=session,
                                             post_id=post_id,
                                             user_id=current_user.id,
                                             reaction_value=reaction)
