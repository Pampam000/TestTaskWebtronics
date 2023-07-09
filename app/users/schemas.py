from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserWithId(BaseModel):
    id: int


class UserCreate(UserBase):
    password: str


class UserInDb(UserBase):
    hashed_password: str


class UserWithToken(UserWithId):
    token: str


class User(UserWithId, UserBase):
    class Config:
        orm_mode = True
