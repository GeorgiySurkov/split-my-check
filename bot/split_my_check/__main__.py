import logging
import sys

import aiohttp_cors
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from aiohttp_pydantic import oas

from .api import api_router
from .database.resource import DatabaseResource
from .di import wire_container
from .settings import settings
from .tg.bot import bot_router

logger = logging.getLogger(__name__)


@web.middleware
async def db_context_middleware(request: web.Request, handler) -> web.Response:
    db = request.app["container"].resolve(DatabaseResource)
    async with db.context():
        return await handler(request)


async def on_bot_startup(bot: Bot) -> None:
    await bot.set_webhook(
        f"{settings.base_url}{settings.webhook_path}",
        secret_token=settings.webhook_secret,
    )


async def di_cleanup(app: web.Application) -> None:
    async with wire_container(settings) as container:
        app["split_my_check_container"] = container
        yield


def main() -> None:
    app = web.Application(middlewares=[db_context_middleware])
    app.cleanup_ctx.append(di_cleanup)

    app.add_routes(api_router)
    oas.setup(app, url_prefix="/docs")

    # aiogram stuff
    dp = Dispatcher()
    dp.include_router(bot_router)
    dp.startup.register(on_bot_startup)
    bot = Bot(settings.bot_token, parse_mode=ParseMode.HTML)

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=settings.webhook_secret,
    )
    webhook_requests_handler.register(app, path=settings.webhook_path)

    setup_application(app, dp, bot=bot)

    # CORS for local development
    if settings.env == "local":
        cors = aiohttp_cors.setup(
            app,
            defaults={
                "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_headers="*",
                )
            },
        )

        # Configure CORS on all routes.
        for route in list(app.router.routes()):
            cors.add(route)

    # And finally start webserver
    logger.info(
        f"Starting web server: {settings.web_server_host=}, {settings.web_server_port=}"
    )
    web.run_app(app, host=settings.web_server_host, port=settings.web_server_port)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
