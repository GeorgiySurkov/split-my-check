import logging

from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200, r404

from split_my_check.state import StateKey
from split_my_check.use_cases.expense_group.get_expense_group.use_case import (
    GetExpenseGroupUseCase,
    GetExpenseGroupOutput,
)
from .utils import parse_expense_group_id
from ..tg.validate import validate_init_data

logger = logging.getLogger(__name__)

api_router = web.RouteTableDef()


@api_router.get("/validate_init_data")
async def validate_init_data_handler(req: web.Request) -> web.Response:
    init_data = validate_init_data(req.query)
    return web.json_response(text=init_data.model_dump_json())


@api_router.view("/expense_group/{group_id}")
class DetailedExpenseGroupView(PydanticView):
    async def get(self, group_id: str, *, username: str) -> r200[GetExpenseGroupOutput] | r404:
        expemse_group_id = parse_expense_group_id(group_id)

        container = self.request.config_dict[StateKey.container]
        uc: GetExpenseGroupUseCase = container.resolve(GetExpenseGroupUseCase)

        output = await uc.execute(group_id=expemse_group_id, username=username)

        return web.json_response(text=output.model_dump_json())
