from pydantic import BaseModel, ConfigDict
from sqlalchemy import select

from split_my_check.database.orm import ExpenseGroup, TelegramUser, User
from split_my_check.database.resource import DatabaseResource
from split_my_check.database.utils import auto_transaction
from split_my_check.schema import ExpenseGroupID, TgUser
from .exc import ExpenseGroupNotFound


class GetExpenseGroupInput(BaseModel):
    group_id: ExpenseGroupID


class GetExpenseGroupOutput(BaseModel):
    name: str
    owner: TgUser

    model_config = ConfigDict(from_attributes=True)


class GetExpenseGroupUseCase:
    def __init__(self, db: DatabaseResource):
        self.db = db

    @auto_transaction()
    async def execute(self, inp: GetExpenseGroupInput) -> GetExpenseGroupOutput:
        res = await self.db.session.execute(
            select(ExpenseGroup, TelegramUser)
            .join(User, ExpenseGroup.owner_id == User.id)
            .join(TelegramUser, User.id == TelegramUser.user_id)
            .where(ExpenseGroup.id == inp.group_id)
        )
        row = res.first()
        if row is None:
            raise ExpenseGroupNotFound()

        return GetExpenseGroupOutput(
            name=row.ExpenseGroup.name, owner=TgUser.model_validate(row.TelegramUser)
        )
