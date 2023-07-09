from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.config import ACCESS_TOKEN_EXPIRE_IN_SECONDS, SECRET_KEY, ALGORITHM
from app.db import get_db
from app.error_mesages import INCORRECT_EMAIL, INCORRECT_PASSWORD
from app.users import schemas, crud
from app.users.models import User
from app.users.schemas import UserInDb

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/log-in/")

ACCESS_TOKEN_EXPIRED = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                     detail='Access token expired')


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


async def authenticate_user(session: AsyncSession,
                            email: str,
                            password: str) -> User:
    user: User = await crud.get_user_by_email(session=session,
                                              email=email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=INCORRECT_EMAIL)

    if not verify_password(password=password,
                           hashed_password=user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=INCORRECT_PASSWORD)

    return user


def create_access_token(email: str) -> str:
    expire: datetime = datetime.utcnow() + timedelta(
        seconds=ACCESS_TOKEN_EXPIRE_IN_SECONDS)

    to_encode = {"sub": email,
                 "exp": expire}

    encoded_jwt: str = jwt.encode(claims=to_encode, key=SECRET_KEY,
                                  algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(session: AsyncSession = Depends(get_db),
                           token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY,
                             algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise ACCESS_TOKEN_EXPIRED

    except JWTError:
        raise ACCESS_TOKEN_EXPIRED

    user: User | None = await crud.get_user_by_email(session=session,
                                                     email=email)
    if not user:
        raise ACCESS_TOKEN_EXPIRED
    return user


async def register_new_user(new_user: schemas.UserCreate,
                            session: AsyncSession) -> User:
    hashed_password: str = hash_password(password=new_user.password)
    user = UserInDb(email=new_user.email,
                    hashed_password=hashed_password)

    user: User = await crud.create_user(session=session, data=user.dict())

    return user
