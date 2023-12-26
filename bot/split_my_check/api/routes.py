import logging

from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200, r404, r403

from split_my_check.state import StateKey
from split_my_check.tg.validate import validate_init_data
from split_my_check.use_cases.expense_group.get_expense_group.use_case import (
    GetExpenseGroupOutput,
    GetExpenseGroupUseCase,
)
from split_my_check.use_cases.expense_group.update_expense_group.use_case import (
    UpdateExpenseGroupInput,
    UpdateExpenseGroupOutput,
    UpdateExpenseGroupUseCase,
)
from .utils import parse_expense_group_id

logger = logging.getLogger(__name__)


api_router = web.RouteTableDef()


@api_router.get("/validate_init_data")
async def validate_init_data_handler(req: web.Request) -> web.Response:
    init_data = validate_init_data(req.query)
    return web.json_response(text=init_data.model_dump_json())


@api_router.view("/expense_group/{group_id}")
class DetailedExpenseGroupView(PydanticView):
    async def get(
        self,
        group_id: str,
        *,
        username: str,
    ) -> r200[GetExpenseGroupOutput] | r404:
        expense_group_id = parse_expense_group_id(group_id)

        container = self.request.config_dict[StateKey.container]
        uc: GetExpenseGroupUseCase = container.resolve(GetExpenseGroupUseCase)

        output = await uc.execute(group_id=expense_group_id, username=username)

        return web.json_response(text=output.model_dump_json())

    async def put(
        self,
        group_id: str,
        inp: UpdateExpenseGroupInput,
        *,
        username: str,
    ) -> r200[UpdateExpenseGroupOutput] | r404 | r403:
        expense_group_id = parse_expense_group_id(group_id)

        container = self.request.config_dict[StateKey.container]
        uc: UpdateExpenseGroupUseCase = container.resolve(UpdateExpenseGroupUseCase)

        output = await uc.execute(inp, username=username, group_id=expense_group_id)

        return web.json_response(text=output.model_dump_json())
