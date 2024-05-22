import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.routers import api_router
from app.core.config import settings
from app.core.exception import (
    ServiceException,
    http_exception_handler,
    service_exception_handler,
    validation_exception_handler,
)


def get_application():
    logger.debug(f"CONF:{settings.__dict__}")

    # init FastAPI APP
    application = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
    )

    # CORS middleware config
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=settings.CORS_ALLOWED_METHODS,
        allow_headers=settings.CORS_ALLOWED_HEADERS,
    )

    # exception handler
    application.add_exception_handler(HTTPException, http_exception_handler)
    application.add_exception_handler(
        RequestValidationError, validation_exception_handler
    )
    application.add_exception_handler(ServiceException, service_exception_handler)

    # router
    application.include_router(api_router, prefix="/api")

    return application


app = get_application()
if __name__ == "__main__":
    uvicorn.run("main:app", **{"host": "0.0.0.0", "port": 8002, "log_level": "info"})
