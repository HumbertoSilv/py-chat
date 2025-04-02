from uuid import UUID

from fastapi import WebSocket


class WebSocketManager:
    def __init__(self):
        self.handlers: dict = {}
        # stores user WebSocket connections
        #  by chat {"chat_guid": {ws1, ws2}, ...}
        self.chats: dict = {}
        # self.pubsub_client = RedisPubSubManager()
        self.user_id_to_websocket: dict = {}

    def handler(self, message_type):
        def decorator(func):
            self.handlers[message_type] = func
            return func

        return decorator

    @staticmethod
    async def connect_socket(websocket: WebSocket):
        await websocket.accept()

    async def add_user_socket_connection(
        self, user_id: UUID, websocket: WebSocket
    ):
        self.user_id_to_websocket.setdefault(user_id, set()).add(websocket)

    async def add_user_to_chat(self, chat_id, websocket: WebSocket):
        if str(chat_id) in self.chats:
            self.chats[str(chat_id)].add(websocket)
        else:
            self.chats[str(chat_id)] = {websocket}

    async def remove_user_guid_to_websocket(
        self, user_id: UUID, websocket: WebSocket
    ):
        if user_id in self.user_id_to_websocket:
            self.user_id_to_websocket.get(user_id).remove(websocket)

    async def remove_user_from_chat(
        self, chat_id: str, websocket: WebSocket
    ) -> None:
        self.chats[str(chat_id)].remove(websocket)
        if len(self.chats[str(chat_id)]) == 0:
            del self.chats[str(chat_id)]

    async def broadcast_to_chat(self, chat_id: UUID, message: str | dict):
        # if isinstance(message, dict):
        #     message = json.dumps(message)

        for connection in self.chats[str(chat_id)]:
            await connection.send_json(message)
