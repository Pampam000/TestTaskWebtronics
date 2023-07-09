from datetime import datetime

from pydantic import BaseModel


class BasePost(BaseModel):
    content: str


class PostWithId(BaseModel):
    id: int


class PostReaction(BaseModel):
    user_id: int
    reaction_value: str

    class Config:
        orm_mode = True


class Post(PostWithId, BasePost):
    user_id: int
    created_at: datetime
    reactions: list[PostReaction] = []

    class Config:
        orm_mode = True
