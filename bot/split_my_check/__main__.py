from aiohttp import web

from .app import create_app
from .settings import settings

if __name__ == "__main__":
    web.run_app(create_app(), host=settings.web_server_host, port=settings.web_server_port)
