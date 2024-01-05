import re

from pydantic import constr, BaseModel, ConfigDict

EXPENSE_GROUP_ID_LEN = 20

PREFIXED_EXPENSE_GROUP_ID_PATTERN = (
    r"^gr([0-9A-Za-z_-]{" + str(EXPENSE_GROUP_ID_LEN) + r"})$"
)
PREFIXED_EXPENSE_GROUP_ID_PATTERN_COMPILED = re.compile(
    PREFIXED_EXPENSE_GROUP_ID_PATTERN
)
EXPENSE_GROUP_ID_PATTERN = r"^[0-9A-Za-z_-]{" + str(EXPENSE_GROUP_ID_LEN) + r"}$"
EXPENSE_GROUP_ID_PATTERN_COMPILED = re.compile(EXPENSE_GROUP_ID_PATTERN)

ExpenseGroupID = constr(pattern=EXPENSE_GROUP_ID_PATTERN)


class PublicTgUser(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    photo_url: str | None = None

    model_config = ConfigDict(from_attributes=True)
