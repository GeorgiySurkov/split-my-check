from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = "prod"
    bot_token: str

    web_server_host: str = "0.0.0.0"
    web_server_port: int = 8080

    webhook_path: str = "/webhook"
    webhook_secret: str = "very-secret-string"
    base_url: str = Field(..., alias="BASE_WEBHOOK_URL")

    postgres_dsn: str = (
        "postgresql+asyncpg://split_my_check:123@localhost:5432/split_my_check"
    )


settings = Settings()
