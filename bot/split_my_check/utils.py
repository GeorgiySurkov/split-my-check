from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import TypeVar, ContextManager

from nanoid import generate

from .schema import EXPENSE_GROUP_ID_LEN, PREFIXED_EXPENSE_GROUP_ID_PATTERN_COMPILED

T = TypeVar("T")


@contextmanager
def set_context(context: ContextVar[T], value: T) -> ContextManager[None]:
    token = context.set(value)
    try:
        yield
    finally:
        context.reset(token)


def now() -> datetime:
    return datetime.now(tz=timezone.utc)


def generate_expense_group_id() -> str:
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz-"
    return generate(alphabet, size=EXPENSE_GROUP_ID_LEN)


def parse_prefixed_expense_group_id(expense_group_id: str) -> str | None:
    match = PREFIXED_EXPENSE_GROUP_ID_PATTERN_COMPILED.match(expense_group_id)
    if match is None:
        return None
    return match.group(1)


def prefix_expense_group_id(expense_group_id: str) -> str:
    return f"gr{expense_group_id}"
