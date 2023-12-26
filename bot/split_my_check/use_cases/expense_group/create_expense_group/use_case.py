from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import insert

from split_my_check.database.orm import ExpenseGroupORM
from split_my_check.database.resource import DatabaseResource
from split_my_check.schema import EXPENSE_GROUP_ID_LEN


class CreateExpenseGroupInput(BaseModel):
    id: str = Field(..., max_length=EXPENSE_GROUP_ID_LEN)
    name: str = Field(..., max_length=64)
    owner_id: UUID


class CreateExpenseGroupOutput(BaseModel):
    id: str
    name: str
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CreateExpenseGroupUseCase:
    def __init__(self, db: DatabaseResource):
        self.db = db

    async def execute(self, inp: CreateExpenseGroupInput) -> CreateExpenseGroupOutput:
        async with self.db.session.begin():
            res = await self.db.session.scalars(
                insert(ExpenseGroupORM)
                .values(inp.model_dump())
                .returning(ExpenseGroupORM)
            )
            expense_group = res.first()
        return CreateExpenseGroupOutput.model_validate(expense_group)
