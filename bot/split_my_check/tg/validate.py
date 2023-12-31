import hashlib
import hmac

from multidict import MultiDictProxy

from .entities import WebAppInitData
from ..exc import InitDataValidationError
from ..settings import settings


def validate_init_data(
    init_data: MultiDictProxy[str],
    token: str = settings.bot_token,
    constant_str: str = "WebAppData",
) -> WebAppInitData:
    """
    Validates the data received from the Telegram web app, using the
    method documented here:
    https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
    """
    if len(init_data) > 10:
        # The data is not from Telegram, so we won't calculate hash.
        raise InitDataValidationError()

    init_data_without_hash = init_data.copy()
    try:
        hash_value = init_data_without_hash.pop("hash")
    except KeyError:
        raise InitDataValidationError()

    # Sorting fields alphabetically.
    init_data_items = list(init_data_without_hash.items())
    init_data_items.sort(key=lambda item: item[0])

    data_check_string = "\n".join(f"{item[0]}={item[1]}" for item in init_data_items)

    secret_key = hmac.new(
        constant_str.encode(), token.encode(), hashlib.sha256
    ).digest()
    data_check = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256)
    if data_check.hexdigest() != hash_value:
        # The data is not from Telegram, so it can't be trusted.
        raise InitDataValidationError()

    return WebAppInitData.model_validate(init_data)
