from typing import Any, Union

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse, ORJSONResponse
from loguru import logger

__all__ = [
    "ServiceException",
    "http_exception_handler",
    "service_exception_handler",
    "validation_exception_handler",
]

from .response import (
    CODE_SERVER_ERROR,
    server_error_response,
    validation_error_response,
)


class ServiceException(HTTPException):
    def __init__(self, message: Any = None, code: str = None) -> None:
        super().__init__(status_code=200, detail=message)
        self.code = code


async def http_exception_handler(
    request: Request,
    exc: Union[HTTPException, ServiceException],
) -> JSONResponse:
    logger.error(
        "http error, api: {api}, error: {error}", api=request.url.path, error=exc.detail
    )
    if hasattr(exc, "code"):
        code = exc.code
    else:
        code = CODE_SERVER_ERROR
    return server_error_response(message=exc.detail, code=code)


async def service_exception_handler(
    request: Request,
    exc: ServiceException,
) -> ORJSONResponse:
    logger.error(
        "service error, api: {api}, error: {error}",
        api=request.url.path,
        error=exc.detail,
    )
    return server_error_response(message=exc.detail)


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> ORJSONResponse:
    logger.error(
        "http error, api: {api}, error: {error}",
        api=request.url.path,
        error=exc.errors(),
    )
    return validation_error_response()
