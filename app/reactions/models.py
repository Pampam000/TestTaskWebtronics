from sqlalchemy import Column, Integer, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db import Base


class UserPostReaction(Base):
    __tablename__ = "users_posts_reactions"
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    reaction_value = Column(String, ForeignKey('reactions.value'))

    post = relationship("Post", back_populates="reactions")
    user = relationship('User', back_populates='reactions')
    UniqueConstraint(user_id, post_id, 'userpost')


class Reaction(Base):
    __tablename__ = "reactions"
    value = Column(String, primary_key=True)
