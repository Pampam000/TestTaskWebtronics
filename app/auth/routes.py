from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db import get_db
from app.users import models
from app.users.schemas import UserCreate, User
from . import auth

router = APIRouter(prefix='/auth',
                   tags=['auth'])


@router.post('/sign-up',
             response_model=User,
             status_code=status.HTTP_201_CREATED)
async def sign_up(user: UserCreate,
                  session: AsyncSession = Depends(get_db)):
    try:
        user: models.User = await auth.register_new_user(session=session,
                                                         new_user=user)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Key (email) = ({user.email}) '
                                   f'already exists')

    return user


@router.post('/log-in/')
async def log_in(session: AsyncSession = Depends(get_db),
                 form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        validated_user = UserCreate(email=form_data.username,
                                    password=form_data.password)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e))

    user: models.User = await auth.authenticate_user(
        session=session, **validated_user.dict())

    access_token: str = auth.create_access_token(email=user.email)
    return {"access_token": access_token, "token_type": "bearer"}
