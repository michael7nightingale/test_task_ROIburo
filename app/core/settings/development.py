from .base import BaseAppSettings


class DevAppSettings(BaseAppSettings):
    LOGGING_LEVEL: str = "INFO"
    DEBUG: bool = True
    DB_URI: str

    class Config:
        env_file = "dev.env"
