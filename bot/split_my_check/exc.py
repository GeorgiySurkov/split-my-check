from aiohttp import web


class InitDataValidationError(web.HTTPBadRequest):
    pass
