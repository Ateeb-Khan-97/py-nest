from fastapi import FastAPI
import fastapi
import fastapi_swagger_dark as fsd

from src.config.env_config import is_production
import logging


def setup_swagger(app: FastAPI) -> None:
    if is_production:
        return

    logger = logging.getLogger(__name__)
    logger.info("Setting up Swagger")
    router = fastapi.APIRouter()
    fsd.install(
        router,
        path="/api/docs",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "syntaxHighlight": {"theme": "obsidian"},
        },
    )
    logger.info("Swagger setup complete")
    app.include_router(router)
