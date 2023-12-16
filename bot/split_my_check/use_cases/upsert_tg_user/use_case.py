from datetime import datetime
from uuid import UUID

from aiogram import types
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from split_my_check.database.orm import TelegramUser, User
from split_my_check.database.resource import DatabaseResource


class UpsertTgUserInput(BaseModel):
    tg_user: types.User


class UpsertTgUserOutput(BaseModel):
    user_id: UUID
    created_at: datetime


class UpsertTgUserUseCase:
    def __init__(self, db: DatabaseResource):
        self.db = db

    async def execute(self, inp: UpsertTgUserInput) -> UpsertTgUserOutput:
        async with self.db.session.begin():
            # check if internal user exists and create if not in one statement
            res = await self.db.session.scalars(
                select(User)
                .join(TelegramUser)
                .where(TelegramUser.tg_id == inp.tg_user.id)
            )
            user = res.first()
            if user is None:
                res = await self.db.session.scalars(
                    insert(User).values().returning(User)
                )
                user = res.first()

            insert_stmt = insert(TelegramUser).values(
                tg_id=inp.tg_user.id,
                username=inp.tg_user.username,
                first_name=inp.tg_user.first_name,
                last_name=inp.tg_user.last_name,
                language_code=inp.tg_user.language_code,
                is_bot=inp.tg_user.is_bot,
                is_premium=inp.tg_user.is_premium,
                user_id=user.id,
            )
            await self.db.session.execute(
                insert_stmt.on_conflict_do_update(
                    index_elements=[TelegramUser.tg_id, TelegramUser.user_id],
                    set_={
                        TelegramUser.username: insert_stmt.excluded.username,
                        TelegramUser.first_name: insert_stmt.excluded.first_name,
                        TelegramUser.last_name: insert_stmt.excluded.last_name,
                        TelegramUser.language_code: insert_stmt.excluded.language_code,
                        TelegramUser.is_bot: insert_stmt.excluded.is_bot,
                        TelegramUser.is_premium: insert_stmt.excluded.is_premium,
                    },
                )
            )

        return UpsertTgUserOutput(
            user_id=user.id,
            created_at=user.created_at,
        )
