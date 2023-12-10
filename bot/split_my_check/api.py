import logging

from aiohttp import web

from .tg.validate import validate_init_data

logger = logging.getLogger(__name__)

api_router = web.RouteTableDef()


@api_router.get("/validate_init_data")
async def validate_init_data_handler(req: web.Request) -> web.Response:
    init_data = validate_init_data(req.query)
    return web.json_response(text=init_data.model_dump_json())
