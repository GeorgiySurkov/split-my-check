from datetime import datetime

from pydantic import BaseModel, Field
from sqlalchemy import insert

from split_my_check.database.orm import ExpenseGroup
from split_my_check.database.resource import DatabaseResource


class CreateExpenseGroupInput(BaseModel):
    id: str = Field(..., max_length=20)
    name: str = Field(..., max_length=64)
    owner_id: str


class CreateExpenseGroupOutput(BaseModel):
    id: str
    name: str
    owner_id: str
    created_at: datetime
    updated_at: datetime


class CreateExpenseGroupUseCase:
    def __init__(self, db: DatabaseResource):
        self.db = db

    async def execute(self, inp: CreateExpenseGroupInput) -> CreateExpenseGroupOutput:
        async with self.db.session.begin():
            expense_group = await self.db.session.scalars(
                insert(ExpenseGroup).values(inp.model_dump()).returning(ExpenseGroup)
            )
        return CreateExpenseGroupOutput.model_validate(expense_group)
