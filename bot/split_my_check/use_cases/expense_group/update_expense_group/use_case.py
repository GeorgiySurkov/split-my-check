from pydantic import BaseModel, ConfigDict
from sqlalchemy import select, update

from split_my_check.database.orm import ExpenseGroupORM, TelegramUserORM, UserORM
from split_my_check.database.resource import DatabaseResource
from split_my_check.database.utils import auto_transaction
from split_my_check.schema import PublicTgUser, ExpenseGroupID
from ...exc import ExpenseGroupNotFound, UserNotFound, NoPermissionToUpdateExpenseGroup


class UpdateExpenseGroupInput(BaseModel):
    name: str


class UpdateExpenseGroupOutput(BaseModel):
    name: str
    owner: PublicTgUser

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
            select(ExpenseGroupORM, TelegramUserORM)
            .join(UserORM, ExpenseGroupORM.owner_id == UserORM.id)
            .join(TelegramUserORM, UserORM.id == TelegramUserORM.user_id)
            .where(ExpenseGroupORM.id == group_id)
        )
        row = res.first()
        if row is None:
            raise ExpenseGroupNotFound()

        res = await self.db.session.scalars(
            select(UserORM)
            .join(TelegramUserORM, UserORM.id == TelegramUserORM.user_id)
            .where(TelegramUserORM.username == username)
        )
        user = res.first()
        if user is None:
            raise UserNotFound()

        # check user has permission to update
        if row.TelegramUser.user_id != user.id:
            raise NoPermissionToUpdateExpenseGroup()

        res = await self.db.session.scalars(
            update(ExpenseGroupORM)
            .where(ExpenseGroupORM.id == group_id)
            .values(name=inp.name)
            .returning(ExpenseGroupORM)
        )
        expense_group = res.first()

        return UpdateExpenseGroupOutput(
            name=expense_group.name,
            owner=PublicTgUser(
                id=row.TelegramUser.tg_id,
                username=row.TelegramUser.username,
                first_name=row.TelegramUser.first_name,
                last_name=row.TelegramUser.last_name,
                photo_url=row.TelegramUser.photo_url,
            ),
        )
