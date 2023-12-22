import logging
from contextlib import asynccontextmanager

from punq import Container, Scope

from .database.resource import DatabaseResource
from .settings import Settings
from .use_cases.create_expense_group.use_case import CreateExpenseGroupUseCase
from .use_cases.upsert_tg_user.use_case import UpsertTgUserUseCase

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

    logger.info("DI container is initialized")
    try:
        yield _container
    finally:
        logger.info("Closing DI container")
        await _container.resolve(DatabaseResource).close()
        logger.info("DI container is closed")
