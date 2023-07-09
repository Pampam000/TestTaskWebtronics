from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError

from app.auth.routes import router as auth_router
from app.db import engine, Base, async_session
from app.posts.routes import router as post_router
from app.reactions.routes import router as reaction_router

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        try:
            await session.execute(
                "INSERT INTO Reactions (value) VALUES ('like'), ('dislike');"
            )
        except IntegrityError:
            pass
        else:
            await session.commit()


app.include_router(auth_router)
app.include_router(post_router)
app.include_router(reaction_router)
