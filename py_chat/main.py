from contextlib import asynccontextmanager

from fastapi import FastAPI

from py_chat.api import websocket
from py_chat.api.routes import friends, users, chats


@asynccontextmanager
async def lifespan(app: FastAPI):
    # logger.info('Starting application')
    yield  # Executa a aplicação
    # logger.info('Stopping application')


app = FastAPI(lifespan=lifespan, title='py-chat')

app.include_router(users.router)
app.include_router(friends.router)
app.include_router(chats.router)
# app.include_router(websocket.websocket_router)
