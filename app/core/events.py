from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.api.routes import routers
from .config import get_app_settings
from .settings.base import BaseAppSettings, AppEnvTypes
from ..service.load_data import load_all_data


async def startup_handler():
    await load_all_data()


def configurate_db(app: FastAPI) -> None:
    register_tortoise(
        app=app,
        config={
                'connections': {
                    'default': get_app_settings().DB_URI
                },
                'apps': {
                    'models': {
                        'models': ['app.models'],
                        'default_connection': 'default',
                    }
                }
            },
        generate_schemas=True
    )


def register_routers(app: FastAPI) -> None:
    for router in routers:
        app.include_router(router, prefix="/api/v1")


def use_production_settings() -> None:
    BaseAppSettings.app_env = AppEnvTypes.prod
