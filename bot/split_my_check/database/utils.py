import typing as t
from contextlib import nullcontext

from sqlalchemy.ext.asyncio import AsyncSession

T = t.TypeVar("T")
P = t.ParamSpec("P")
FuncToBeDecorated = t.Callable[P, t.Awaitable[T]]
DecoratedFunc = t.Callable[P, t.Awaitable[T]]


def auto_transaction(
    *,
    default_in_transaction: bool = True,
    default_nested: bool = False,
    session_getter: t.Callable[P, AsyncSession] | None = None,
) -> t.Callable[[FuncToBeDecorated], DecoratedFunc]:
    """Декоратор, который автоматически выполняет функцию внутри транзакции БД.

    :param default_in_transaction: Выполняется ли метод внутри транзакции по умолчанию.
    :param default_nested: Выполняется ли метода во вложенной транзакции по умолчанию.
    :param session_getter: Геттер для сессии. По умолчанию дергает self.db.session.
    """

    def _decorator(f: FuncToBeDecorated):
        async def _wrapper(
            *args: P.args,
            in_transaction=default_in_transaction,
            nested=default_nested,
            **kwargs: P.kwargs,
        ):
            # FIXME: Сейчас пока нельзя с помощью типов показать, что декоратор
            #  добавляет key-word аргументы функции.
            #  Исправить это, когда появится такая возможность.
            session: AsyncSession
            if session_getter is None:
                try:
                    session = args[0].db.session
                except AttributeError:
                    raise TypeError("Repository session not found")
            else:
                session = session_getter(*args, **kwargs)

            if in_transaction and nested:
                transaction = session.begin_nested()
            elif in_transaction:
                transaction = session.begin()
            else:
                transaction = nullcontext

            async with transaction:
                return await f(*args, **kwargs)

        return _wrapper

    return _decorator
