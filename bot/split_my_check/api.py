import logging

from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200
from pydantic import ValidationError

from split_my_check.state import StateKey
from split_my_check.use_cases.expense_group.get_expense_group.use_case import (
    GetExpenseGroupUseCase,
    GetExpenseGroupOutput,
    GetExpenseGroupInput,
)
from .tg.validate import validate_init_data

logger = logging.getLogger(__name__)

api_router = web.RouteTableDef()


@api_router.get("/validate_init_data")
async def validate_init_data_handler(req: web.Request) -> web.Response:
    init_data = validate_init_data(req.query)
    return web.json_response(text=init_data.model_dump_json())


@api_router.view("/expense_group/{group_id}")
class DetailedExpenseGroupView(PydanticView):
    async def get(self, group_id: str, *, username: str) -> r200[GetExpenseGroupOutput]:
        try:
            inp = GetExpenseGroupInput(group_id=group_id)
        except ValidationError as e:
            return web.json_response(text=e.json(), status=400)

        container = self.request.config_dict[StateKey.container]
        uc: GetExpenseGroupUseCase = container.resolve(GetExpenseGroupUseCase)

        output = await uc.execute(inp, username)

        return web.json_response(text=output.model_dump_json())
