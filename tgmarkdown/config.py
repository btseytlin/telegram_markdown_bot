from confi import BaseEnvironConfig, ConfigField, IntConfig


class Config(BaseEnvironConfig):
    TG_API_TOKEN = ConfigField(required=True)
    ADMIN_UID = IntConfig(required=True)
    WEBHOOK_PORT = IntConfig(required=False)
    HEROKU_NAME = ConfigField(required=False)

