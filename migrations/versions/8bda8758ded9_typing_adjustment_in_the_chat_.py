"""typing adjustment in the chat_participants table

Revision ID: 8bda8758ded9
Revises: 15d9aa140343
Create Date: 2025-02-08 20:15:34.335977

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '8bda8758ded9'
down_revision: Union[str, None] = '15d9aa140343'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Remover as chaves estrangeiras temporariamente
    op.drop_constraint("chat_participants_user_id_fkey",
                       "chat_participants", type_="foreignkey")
    op.drop_constraint("friends_user_id_fkey", "friends", type_="foreignkey")
    op.drop_constraint("friends_friend_id_fkey", "friends", type_="foreignkey")
    op.drop_constraint("messages_user_id_fkey", "messages", type_="foreignkey")

    # Alterar as colunas de VARCHAR para UUID
    op.execute(
        "ALTER TABLE chat_participants ALTER COLUMN user_id TYPE UUID USING user_id::uuid")
    op.execute(
        "ALTER TABLE friends ALTER COLUMN user_id TYPE UUID USING user_id::uuid")
    op.execute(
        "ALTER TABLE friends ALTER COLUMN friend_id TYPE UUID USING friend_id::uuid")
    op.execute(
        "ALTER TABLE messages ALTER COLUMN user_id TYPE UUID USING user_id::uuid")
    op.execute("ALTER TABLE users ALTER COLUMN id TYPE UUID USING id::uuid")

    # Recriar as chaves estrangeiras com o novo tipo UUID
    op.create_foreign_key(
        "chat_participants_user_id_fkey", "chat_participants", "users",
        ["user_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        "friends_user_id_fkey", "friends", "users",
        ["user_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        "friends_friend_id_fkey", "friends", "users",
        ["friend_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        "messages_user_id_fkey", "messages", "users",
        ["user_id"], ["id"], ondelete="CASCADE"
    )


def downgrade() -> None:
    # Remover as chaves estrangeiras antes de voltar para VARCHAR
    op.drop_constraint("chat_participants_user_id_fkey",
                       "chat_participants", type_="foreignkey")
    op.drop_constraint("friends_user_id_fkey", "friends", type_="foreignkey")
    op.drop_constraint("friends_friend_id_fkey", "friends", type_="foreignkey")
    op.drop_constraint("messages_user_id_fkey", "messages", type_="foreignkey")

    # Alterar as colunas de UUID de volta para VARCHAR
    op.execute(
        "ALTER TABLE chat_participants ALTER COLUMN user_id TYPE VARCHAR USING user_id::text")
    op.execute(
        "ALTER TABLE friends ALTER COLUMN user_id TYPE VARCHAR USING user_id::text")
    op.execute(
        "ALTER TABLE friends ALTER COLUMN friend_id TYPE VARCHAR USING friend_id::text")
    op.execute(
        "ALTER TABLE messages ALTER COLUMN user_id TYPE VARCHAR USING user_id::text")
    op.execute("ALTER TABLE users ALTER COLUMN id TYPE VARCHAR USING id::text")

    # Recriar as chaves estrangeiras com o tipo VARCHAR
    op.create_foreign_key(
        "chat_participants_user_id_fkey", "chat_participants", "users",
        ["user_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        "friends_user_id_fkey", "friends", "users",
        ["user_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        "friends_friend_id_fkey", "friends", "users",
        ["friend_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        "messages_user_id_fkey", "messages", "users",
        ["user_id"], ["id"], ondelete="CASCADE"
    )
