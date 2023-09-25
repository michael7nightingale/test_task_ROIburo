from fastapi import FastAPI
import os

from app.core.events import (
    startup_handler,
    register_routers,
    use_production_settings,
    configurate_db,

)


def create_app(*args, **kwargs) -> FastAPI:
    """Application factory function."""
    app = FastAPI()
    register_routers(app)

    if os.getenv("PROD"):   # checks if to use production environment
        use_production_settings()

    configurate_db(app)
    app.add_event_handler("startup", startup_handler)

    return app
