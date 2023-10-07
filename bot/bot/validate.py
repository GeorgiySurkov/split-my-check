from dataclasses import dataclass
import hmac
import hashlib
from urllib.parse import unquote

from .tg_entities import WebAppInitData
from . import settings
from .exc import InitDataValidationError


def validate(init_data: str, token: str = settings.BOT_TOKEN, c_str="WebAppData") -> WebAppInitData:
    """
    Validates the data received from the Telegram web app, using the
    method documented here:
    https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
    """
    hash_str = None
    init_data_items = []
    for item in unquote(init_data).split("&"):
        split_item = item.split("=", maxsplit=1)
        try:
            key, value = split_item
        except ValueError:  # Can't split item with '='
            raise InitDataValidationError()

        if key == "hash":
            if hash_str is not None:  # hash was encountered more than once
                raise InitDataValidationError()
            hash_str = value
        else:
            init_data_items.append((key, value))

    # Sorting fields alphabetically.
    init_data_items.sort(key=lambda item: item[0])

    data_check_string = "\n".join(f"{item[0]}={item[1]}" for item in init_data_items)

    secret_key = hmac.new(
        c_str.encode(),
        token.encode(),
        hashlib.sha256
    ).digest()
    data_check = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    )
    if data_check.hexdigest() != hash_str:
        # The data is not from Telegram, so it can't be trusted.
        raise InitDataValidationError()

    return WebAppInitData.model_validate(dict(init_data_items))
