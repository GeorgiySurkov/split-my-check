import logging
from contextlib import asynccontextmanager

from punq import Container, Scope

from .database.resource import DatabaseResource
from .settings import Settings
from .use_cases.create_expense_group.use_case import CreateExpenseGroupUseCase
from .use_cases.upsert_tg_user.use_case import UpsertTgUserUseCase

logger = logging.getLogger(__name__)


@asynccontextmanager
async def wire_container(settings: Settings) -> Container:
    logger.info("Initializing DI container")
    container = Container()

    container.register(Settings, instance=settings)
    container.register(DatabaseResource, scope=Scope.singleton)

    # Use cases
    container.register(CreateExpenseGroupUseCase, scope=Scope.singleton)
    container.register(UpsertTgUserUseCase, scope=Scope.singleton)

    logger.info("DI container is initialized")
    try:
        yield container
    finally:
        logger.info("Closing DI container")
        await container.resolve(DatabaseResource).close()
        logger.info("DI container is closed")
