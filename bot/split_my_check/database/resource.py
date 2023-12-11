import asyncio as aio
import logging
from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import AsyncIterator

from asyncpg import PostgresError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from split_my_check import settings
from split_my_check.utils import set_context

logger = logging.getLogger(__name__)


class DatabaseResource:
    def __init__(self):
        self.engine = create_async_engine(
            settings.POSTGRES_DSN,
            echo=True,
        )
        self._new_session = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
        )
        self._current_session: ContextVar[AsyncSession | None] = ContextVar(
            "current_postgres_session", default=None
        )

    def get_session(self) -> AsyncSession:
        session = self._current_session.get()
        if session is None:
            raise RuntimeError("No database context")
        return session

    @property
    def session(self) -> AsyncSession:
        return self.get_session()

    @asynccontextmanager
    async def context(self) -> AsyncIterator[None]:
        if self._current_session.get() is not None:
            raise RuntimeError("Database context is already set")

        async with self._new_session() as session:
            with set_context(self._current_session, session):
                logger.debug("DB session is set: %session", dict(session=session))
                yield
        logger.debug("DB session is closed: %session", dict(session=session))

    async def is_health(self, *, timeout: float | None = None) -> bool:
        try:
            await aio.wait_for(self.session.execute(text("SELECT 1")), timeout=timeout)
        except (SQLAlchemyError, PostgresError, aio.TimeoutError, TimeoutError):
            return False
        return True

    async def close(self) -> None:
        await self.engine.dispose()
        logger.debug("DB engine is closed")
