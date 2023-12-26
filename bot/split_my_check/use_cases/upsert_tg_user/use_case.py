from datetime import datetime
from uuid import UUID

from aiogram import types
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from split_my_check.database.orm import TelegramUserORM, UserORM
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
                select(UserORM)
                .join(TelegramUserORM)
                .where(TelegramUserORM.tg_id == inp.tg_user.id)
            )
            user = res.first()
            if user is None:
                res = await self.db.session.scalars(
                    insert(UserORM).values().returning(UserORM)
                )
                user = res.first()

            insert_stmt = insert(TelegramUserORM).values(
                tg_id=inp.tg_user.id,
                username=inp.tg_user.username,
                first_name=inp.tg_user.first_name,
                last_name=inp.tg_user.last_name,
                language_code=inp.tg_user.language_code,
                is_bot=inp.tg_user.is_bot,
                is_premium=inp.tg_user.is_premium,
                user_id=user.id,
            )
            on_conflict_set = {
                TelegramUserORM.first_name: insert_stmt.excluded.first_name,
                TelegramUserORM.last_name: insert_stmt.excluded.last_name,
                TelegramUserORM.is_bot: insert_stmt.excluded.is_bot,
                TelegramUserORM.is_premium: insert_stmt.excluded.is_premium,
            }
            if inp.tg_user.username is not None:
                on_conflict_set[
                    TelegramUserORM.username
                ] = insert_stmt.excluded.username
            if inp.tg_user.language_code is not None:
                on_conflict_set[
                    TelegramUserORM.language_code
                ] = insert_stmt.excluded.language_code
            if inp.tg_user.is_premium is not None:
                on_conflict_set[
                    TelegramUserORM.is_premium
                ] = insert_stmt.excluded.is_premium

            await self.db.session.execute(
                insert_stmt.on_conflict_do_update(
                    index_elements=[TelegramUserORM.tg_id],
                    set_=on_conflict_set,
                )
            )

        return UpsertTgUserOutput(
            user_id=user.id,
            created_at=user.created_at,
        )
