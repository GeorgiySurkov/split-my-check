from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from split_my_check.database.orm import TelegramUserORM, UserORM
from split_my_check.database.resource import DatabaseResource
from split_my_check.database.utils import auto_transaction
from split_my_check.schema import PublicTgUser


class UpsertTgUserInput(BaseModel):
    id: int
    username: str | None = None
    first_name: str
    last_name: str | None = None
    language_code: str | None = None
    is_bot: bool | None = None
    is_premium: bool | None = None
    added_to_attachment_menu: bool | None = None
    allows_write_to_pm: bool | None = None
    photo_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UpsertTgUserOutput(BaseModel):
    user_id: UUID
    tg_user: PublicTgUser
    created_at: datetime


class UpsertTgUserUseCase:
    def __init__(self, db: DatabaseResource):
        self.db = db

    @auto_transaction()
    async def execute(self, inp: UpsertTgUserInput) -> UpsertTgUserOutput:
        # check if internal user exists and create if not in one statement
        res = await self.db.session.scalars(
            select(UserORM).join(TelegramUserORM).where(TelegramUserORM.tg_id == inp.id)
        )
        user = res.first()
        if user is None:
            res = await self.db.session.scalars(
                insert(UserORM).values().returning(UserORM)
            )
            user = res.first()

        without_unset = inp.model_dump(exclude_unset=True)
        insert_stmt = insert(TelegramUserORM).values(
            user_id=user.id,
            tg_id=inp.id,
            username=inp.username,
            first_name=inp.first_name,
            last_name=inp.last_name,
            language_code=inp.language_code,
            is_bot=inp.is_bot,
            is_premium=inp.is_premium,
            added_to_attachment_menu=inp.added_to_attachment_menu,
            allows_write_to_pm=inp.allows_write_to_pm,
            photo_url=inp.photo_url,
        )
        on_conflict_set = {
            TelegramUserORM.first_name: insert_stmt.excluded.first_name,
            TelegramUserORM.last_name: insert_stmt.excluded.last_name,
        }
        if "username" in without_unset:
            on_conflict_set[TelegramUserORM.username] = insert_stmt.excluded.username
        if "language_code" in without_unset:
            on_conflict_set[
                TelegramUserORM.language_code
            ] = insert_stmt.excluded.language_code
        if "is_bot" in without_unset:
            on_conflict_set[TelegramUserORM.is_bot] = insert_stmt.excluded.is_bot
        if "is_premium" in without_unset:
            on_conflict_set[
                TelegramUserORM.is_premium
            ] = insert_stmt.excluded.is_premium
        if "added_to_attachment_menu" in without_unset:
            on_conflict_set[
                TelegramUserORM.added_to_attachment_menu
            ] = insert_stmt.excluded.added_to_attachment_menu
        if "allows_write_to_pm" in without_unset:
            on_conflict_set[
                TelegramUserORM.allows_write_to_pm
            ] = insert_stmt.excluded.allows_write_to_pm
        if "photo_url" in without_unset:
            on_conflict_set[TelegramUserORM.photo_url] = insert_stmt.excluded.photo_url

        tg_user = await self.db.session.scalar(
            insert_stmt.on_conflict_do_update(
                index_elements=[TelegramUserORM.tg_id],
                set_=on_conflict_set,
            ).returning(TelegramUserORM)
        )

        return UpsertTgUserOutput(
            user_id=user.id,
            created_at=user.created_at,
            tg_user=PublicTgUser(
                id=tg_user.tg_id,
                username=tg_user.username,
                first_name=tg_user.first_name,
                last_name=tg_user.last_name,
                photo_url=tg_user.photo_url,
            ),
        )
