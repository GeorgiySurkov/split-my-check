from pydantic import BaseModel


class UpdateExpenseGroupInput(BaseModel):
    name: str
