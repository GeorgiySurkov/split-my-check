from uuid import UUID

from aiohttp import web
from aiohttp_session import get_session, new_session
from pydantic import BaseModel, Field, ValidationError


class Identity(BaseModel):
    user_id: UUID = Field(..., alias="u")
    tg_id: int | None = Field(None, alias="tg")


class IdentityPolicy:
    def __init__(self, session_key: str = "AIOHTTP_SECURITY"):
        self._session_key = session_key

    @staticmethod
    def _parse_identity_or_none(raw_identity: str) -> Identity | None:
        try:
            return Identity.model_validate_json(raw_identity)
        except ValidationError:
            return None

    @staticmethod
    def _dump_identity(identity: Identity) -> str:
        return identity.model_dump_json(by_alias=True)

    async def identify(self, request: web.Request) -> Identity | None:
        session = await get_session(request)
        raw_identity = session.get(self._session_key)
        if raw_identity is None:
            return None
        return self._parse_identity_or_none(raw_identity)

    async def remember(
        self,
        request: web.Request,
        response: web.StreamResponse,
        identity: Identity,
        **kwargs: None,
    ) -> None:
        session = await new_session(request)
        session[self._session_key] = self._dump_identity(identity)

    async def forget(self, request: web.Request, response: web.StreamResponse) -> None:
        session = await get_session(request)
        session.pop(self._session_key, None)
