import logging

from aiogram import Router, types
from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200

from .tg.entities import WebAppInitData
from .tg.validate import validate_init_data
from . import settings

# All handlers should be attached to the Router (or Dispatcher)
bot_router = Router()
api_routes = web.RouteTableDef()

logger = logging.getLogger(__name__)


@bot_router.inline_query()
async def handle_inline_query(q: types.InlineQuery) -> None:
    logger.info(f"Incoming inline request")
    await q.answer(
        results=[
            types.InlineQueryResultArticle(
                id="1",
                title="Создать трикаунт",
                description="Будет отправлено сообщение, по которому можно будет зайти в нужный трикаунт",
                input_message_content=types.InputTextMessageContent(
                    message_text="А вот и трикаунт: https://t.me/splitmycheckbot/app?startapp=gr123",
                )
            )
        ],
        cache_time=0,
    )


# echo incoming message to bot
@bot_router.message()
async def handle_message(msg: types.Message) -> None:
    logger.info(f"Incoming message: {msg.text}")
    await msg.answer(msg.text)


@api_routes.get("/validate_init_data")
async def validate_init_data_handler(req: web.Request) -> web.Response:
    init_data = validate_init_data(req.query)
    print(req.query)
    return web.json_response(text=init_data.model_dump_json())
