import logging

from aiogram import Router, types

from split_my_check.di import get_container
from split_my_check.use_cases.expense_group.create_expense_group import (
    CreateExpenseGroupUseCase,
    CreateExpenseGroupInput,
)
from split_my_check.use_cases.upsert_tg_user import (
    UpsertTgUserUseCase,
    UpsertTgUserInput,
)
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
    logger.info(
        f"Incoming inline request: "
        f"{q.id=}, {q.query=}, {q.from_user.username=}, {q.from_user.id=}, {q.from_user.language_code=}"
    )

    if len(q.query) > 256:
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
                title="Создать группу расходов",
                description=f'Будет отправлено сообщение с ссылкой на новую группу расходов "{q.query}". '
                f"Название группы можно будет изменить.",
                input_message_content=types.InputTextMessageContent(
                    message_text=f'А вот и новая группа расходов "{q.query}": https://t.me/splitmycheckbot/app?startapp={prefixed_expense_group_id}',
                ),
            )
        ],
        cache_time=0,
        is_personal=True,
    )


@bot_router.chosen_inline_result()
async def handle_chosen_inline_result(q: types.ChosenInlineResult) -> None:
    logger.info(
        f"Incoming chosen inline result: "
        f"{q.result_id=}, {q.query=}, {q.from_user.username=}, {q.from_user.id=}, {q.from_user.language_code=}"
    )

    expense_group_id = parse_prefixed_expense_group_id(q.result_id)
    if expense_group_id is None:
        logger.warning(f"Invalid expense group id: {q.result_id}")
        return
    logger.info(f"Expense group id: {expense_group_id}")

    container = get_container()
    uc: UpsertTgUserUseCase = container.resolve(UpsertTgUserUseCase)
    output = await uc.execute(
        UpsertTgUserInput.model_validate(q.from_user.model_dump(exclude_unset=True))
    )

    uc: CreateExpenseGroupUseCase = container.resolve(CreateExpenseGroupUseCase)
    await uc.execute(
        CreateExpenseGroupInput(
            id=expense_group_id,
            name=q.query,
            owner_id=output.user_id,
        )
    )


# echo incoming message to bot
@bot_router.message()
async def handle_message(msg: types.Message) -> None:
    logger.info(f"Incoming message: {msg.text}")
    await msg.answer(msg.text)
