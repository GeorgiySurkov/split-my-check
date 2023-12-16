from pydantic import BaseModel, Field
from sqlalchemy import insert

from split_my_check.database.orm import ExpenseGroup
from split_my_check.database.resource import DatabaseResource


class CreateExpenseGroupInput(BaseModel):
    id: str = Field(..., max_length=20)
    name: str = Field(..., max_length=64)


CreateExpenseGroupOutput = None


class CreateExpenseGroupUseCase:
    def __init__(self, db: DatabaseResource):
        self.db = db

    async def execute(self, inp: CreateExpenseGroupInput) -> CreateExpenseGroupOutput:
        async with self.db.session.begin():
            await self.db.session.execute(insert(ExpenseGroup).values(inp.model_dump()))
