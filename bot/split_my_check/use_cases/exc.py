from aiohttp.web_exceptions import HTTPNotFound, HTTPForbidden


class ExpenseGroupNotFound(HTTPNotFound):
    """Expense group not found."""


class UserNotFound(HTTPNotFound):
    """User not found."""


class NoPermissionToUpdateExpenseGroup(HTTPForbidden):
    """User has no permission to update expense group."""
