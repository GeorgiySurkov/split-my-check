import logging


from aiohttp import web
from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from . import settings

# All handlers should be attached to the Router (or Dispatcher)
bot_router = Router()
api_routes = web.RouteTableDef()

logger = logging.getLogger(__name__)


@bot_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


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
        cache_time=1,
    )


@api_routes.post("/validated_init_data")
async def get_validated_init_data(req: web.Request) -> web.Response:
    data = await req.json()
    init_data = data["init_data"]

