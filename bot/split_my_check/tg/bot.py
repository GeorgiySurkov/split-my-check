import logging

from aiogram import Router, types

# All handlers should be attached to the Router (or Dispatcher)
bot_router = Router()

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
