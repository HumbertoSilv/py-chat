from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from py_chat.api.routes import auth, chats, friends, users
from py_chat.api.websocket import websocket


@asynccontextmanager
async def lifespan(app: FastAPI):
    # logger.info('Starting application')
    yield  # Start the application
    # logger.info('Stopping application')


app = FastAPI(lifespan=lifespan, title='py-chat')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],  # Next.js
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(users.router)
app.include_router(friends.router)
app.include_router(chats.router)
app.include_router(auth.router)
app.include_router(websocket.websocket_router)
