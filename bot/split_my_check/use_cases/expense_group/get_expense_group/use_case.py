from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from split_my_check.database.orm import (
    ExpenseGroup,
    TelegramUser,
    User,
    ExpenseGroupParticipant,
)
from split_my_check.database.resource import DatabaseResource
from split_my_check.database.utils import auto_transaction
from split_my_check.schema import ExpenseGroupID, TgUser
from split_my_check.use_cases.exc import ExpenseGroupNotFound, UserNotFound


class GetExpenseGroupOutput(BaseModel):
    name: str
    owner: TgUser

    model_config = ConfigDict(from_attributes=True)


class GetExpenseGroupUseCase:
    def __init__(self, db: DatabaseResource):
        self.db = db

    @auto_transaction()
    async def execute(
        self,
        *,
        group_id: ExpenseGroupID,
        username: str,
    ) -> GetExpenseGroupOutput:
        res = await self.db.session.execute(
            select(ExpenseGroup, TelegramUser)
            .join(User, ExpenseGroup.owner_id == User.id)
            .join(TelegramUser, User.id == TelegramUser.user_id)
            .where(ExpenseGroup.id == group_id)
        )
        row = res.first()
        if row is None:
            raise ExpenseGroupNotFound()

        res = await self.db.session.scalars(
            select(User)
            .join(TelegramUser, User.id == TelegramUser.user_id)
            .where(TelegramUser.username == username)
        )
        user = res.first()
        if user is None:
            raise UserNotFound()

        await self.db.session.execute(
            insert(ExpenseGroupParticipant)
            .values(
                expense_group_id=group_id,
                user_id=user.id,
            )
            .on_conflict_do_nothing()
        )

        return GetExpenseGroupOutput(
            name=row.ExpenseGroup.name, owner=TgUser.model_validate(row.TelegramUser)
        )
