import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Webserver settings
# bind localhost only to prevent any external access
WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST", "0.0.0.0")
# Port for incoming request from reverse proxy. Should be any available port
WEB_SERVER_PORT = os.getenv("WEB_SERVER_PORT", 8080)

# Path to webhook route, on which Telegram will send requests
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")
# Secret key to validate requests from Telegram (optional)
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "very-secret-string")
# Base URL for webhook will be used to generate webhook URL for Telegram,
# in this example it is used public DNS with HTTPS support
BASE_WEBHOOK_URL = os.getenv("BASE_WEBHOOK_URL")
