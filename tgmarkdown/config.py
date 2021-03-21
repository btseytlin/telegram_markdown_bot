from confi import BaseEnvironConfig, ConfigField, IntConfig


class Config(BaseEnvironConfig):
    TG_API_TOKEN = ConfigField(required=True)
    ADMIN_UID = IntConfig(required=True)
