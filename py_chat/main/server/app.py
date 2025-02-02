from contextlib import asynccontextmanager

from fastapi import FastAPI

from py_chat.main.routers import friends, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # logger.info('Starting application')
    yield  # Executa a aplicação
    # logger.info('Stopping application')


app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(friends.router)
