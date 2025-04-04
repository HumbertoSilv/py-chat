import asyncio

from py_chat.core.database import AsyncSessionFactory
from py_chat.models.user import Chat, ChatParticipant, ChatType, User


async def run_seed():
    async with AsyncSessionFactory() as session:
        try:
            # create new users
            user1 = User(username='user1', email='user1@example.com')
            user2 = User(username='user2', email='user2@example.com')
            session.add_all([user1, user2])
            await session.commit()

            # create new Chat
            chat = Chat(chat_type=ChatType.DIRECT)
            session.add(chat)

            participant1 = ChatParticipant(user_id=user1.id, chat_id=chat.id)
            participant2 = ChatParticipant(user_id=user2.id, chat_id=chat.id)
            session.add_all([participant1, participant2])
            await session.commit()

            print('Seed data inserted successfully!')

        except Exception as error:
            session.rollback()
            raise error


if __name__ == '__main__':
    asyncio.run(run_seed())
