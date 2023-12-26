import logging
from contextlib import asynccontextmanager

from punq import Container, Scope

from split_my_check.use_cases.expense_group.create_expense_group import (
    CreateExpenseGroupUseCase,
)
from split_my_check.use_cases.expense_group.get_expense_group.use_case import (
    GetExpenseGroupUseCase,
)
from split_my_check.use_cases.expense_group.update_expense_group.use_case import (
    UpdateExpenseGroupUseCase,
)
from split_my_check.use_cases.upsert_tg_user.use_case import UpsertTgUserUseCase
from .database.resource import DatabaseResource
from .settings import Settings

logger = logging.getLogger(__name__)


_container: Container | None = None


def get_container() -> Container:
    if _container is None:
        raise RuntimeError("DI container is not wired")
    return _container


@asynccontextmanager
async def wire_container(settings: Settings) -> Container:
    global _container
    logger.info("Initializing DI container")
    _container = Container()

    _container.register(Settings, instance=settings)
    _container.register(DatabaseResource, scope=Scope.singleton)

    # Use cases
    _container.register(CreateExpenseGroupUseCase, scope=Scope.singleton)
    _container.register(UpsertTgUserUseCase, scope=Scope.singleton)
    _container.register(GetExpenseGroupUseCase, scope=Scope.singleton)
    _container.register(UpdateExpenseGroupUseCase, scope=Scope.singleton)

    logger.info("DI container is initialized")
    try:
        yield _container
    finally:
        logger.info("Closing DI container")
        await _container.resolve(DatabaseResource).close()
        logger.info("DI container is closed")
