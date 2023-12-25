from aiohttp.web_exceptions import HTTPNotFound


class ExpenseGroupNotFound(HTTPNotFound):
    """Expense group not found."""
