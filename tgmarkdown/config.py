from confi import BaseEnvironConfig, ConfigField

class Config(BaseEnvironConfig):
    TG_API_TOKEN = ConfigField(required=True)
