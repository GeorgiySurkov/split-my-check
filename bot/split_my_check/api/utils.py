from pydantic import ValidationError, TypeAdapter

from split_my_check.schema import ExpenseGroupID
from split_my_check.use_cases.exc import ExpenseGroupNotFound


def parse_expense_group_id(group_id: str) -> ExpenseGroupID:
    try:
        return TypeAdapter(ExpenseGroupID).validate_python(group_id)
    except ValidationError:
        raise ExpenseGroupNotFound()
