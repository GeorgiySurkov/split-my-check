import logging

from aiogram import Router, types

from split_my_check.utils import (
    generate_expense_group_id,
    prefix_expense_group_id,
    parse_prefixed_expense_group_id,
)

# All handlers should be attached to the Router (or Dispatcher)
bot_router = Router()

logger = logging.getLogger(__name__)


@bot_router.inline_query()
async def handle_inline_query(q: types.InlineQuery) -> None:
    logger.info(f"Incoming inline request: {q.id=}, {q.query=}")
    if len(q.query) > 64:
        # Too long query
        await q.answer(
            results=[],
            cache_time=0,
            is_personal=True,
        )
        return

    expense_group_id = generate_expense_group_id()
    prefixed_expense_group_id = prefix_expense_group_id(expense_group_id)
    logger.info(
        f"Generated expense group id: {expense_group_id=}, {prefixed_expense_group_id=}"
    )

    await q.answer(
        results=[
            types.InlineQueryResultArticle(
                id=prefixed_expense_group_id,
                title="Создать трикаунт",
                description=f'Будет отправлено сообщение с ссылкой на новую группу расходов "{q.query}"',
                input_message_content=types.InputTextMessageContent(
                    message_text=f"А вот и трикаунт: https://t.me/splitmycheckbot/app?startapp={prefixed_expense_group_id}",
                ),
            )
        ],
        cache_time=0,
        is_personal=True,
    )


@bot_router.chosen_inline_result()
async def handle_chosen_inline_result(q: types.ChosenInlineResult) -> None:
    logger.info(f"Incoming chosen inline result: {q.result_id=}, {q.query=}")
    expense_group_id = parse_prefixed_expense_group_id(q.result_id)
    if expense_group_id is None:
        logger.warning(f"Invalid expense group id: {q.result_id}")
        return
    logger.info(f"Expense group id: {expense_group_id}")


# echo incoming message to bot
@bot_router.message()
async def handle_message(msg: types.Message) -> None:
    logger.info(f"Incoming message: {msg.text}")
    await msg.answer(msg.text)
