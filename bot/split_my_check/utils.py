from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import TypeVar, ContextManager

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
