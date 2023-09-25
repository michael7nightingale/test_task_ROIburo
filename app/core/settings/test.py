from .base import BaseAppSettings


class TestAppSettings(BaseAppSettings):
    LOGGING_LEVEL: str = "INFO"
    DEBUG: bool = False
    DB_URI: str

    class Config:
        env_file = "test.env"
