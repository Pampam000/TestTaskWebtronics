from enum import Enum

from pydantic import BaseModel


class Reaction(Enum):
    like = 'like'
    dislike = 'dislike'


class BaseUserPostReaction(BaseModel):
    user_id: int
    post_id: int
    reaction_value: Reaction


class UserPostReaction(BaseUserPostReaction):
    id: int

    class Config:
        orm_mode = True
