from pydantic import BaseModel, ConfigDict
from sqlalchemy import select, update

from split_my_check.database.orm import ExpenseGroup, TelegramUser, User
from split_my_check.database.resource import DatabaseResource
from split_my_check.database.utils import auto_transaction
from split_my_check.schema import TgUser, ExpenseGroupID
from ...exc import ExpenseGroupNotFound, UserNotFound, NoPermissionToUpdateExpenseGroup


class UpdateExpenseGroupInput(BaseModel):
    name: str


class UpdateExpenseGroupOutput(BaseModel):
    name: str
    owner: TgUser

    model_config = ConfigDict(from_attributes=True)


class UpdateExpenseGroupUseCase:
    def __init__(self, db: DatabaseResource):
        self.db = db

    @auto_transaction()
    async def execute(
        self,
        inp: UpdateExpenseGroupInput,
        *,
        username: str,
        group_id: ExpenseGroupID,
    ) -> UpdateExpenseGroupOutput:
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

        # check user has permission to update
        if row.TelegramUser.user_id != user.id:
            raise NoPermissionToUpdateExpenseGroup()

        res = await self.db.session.scalars(
            update(ExpenseGroup)
            .where(ExpenseGroup.id == group_id)
            .values(name=inp.name)
            .returning(ExpenseGroup)
        )
        expense_group = res.first()

        return UpdateExpenseGroupOutput(
            name=expense_group.name, owner=TgUser.model_validate(row.TelegramUser)
        )
