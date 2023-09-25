from .base import BaseAppSettings


class ProdAppSettings(BaseAppSettings):
    LOGGING_LEVEL: str = "ERROR"
    DEBUG: bool = False
    DB_URI: str

    class Config:
        env_file = "prod.env"
