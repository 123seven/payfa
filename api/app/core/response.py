import decimal
from enum import Enum
from typing import Any, Dict, List

import orjson
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel

__all__ = [
    "BaseResponse",
    "ResponseModel",
    "ListDataSchema",
    "ListResponseModel",
    "ServiceResult",
    "SuccessResult",
    "ErrorResult",
    "common_response",
    "success_response",
    "error_response",
    "server_error_response",
    "validation_error_response",
    "CODE_SERVER_ERROR",
    "AUTH_ERROR",
]

CODE_SUCCESS = "SUCCESS"
CODE_ERROR = "ERROR"
CODE_SERVER_ERROR = "SERVICE_ERROR"
CODE_PARAMS_ERROR = "PARAMS_ERROR"
CODE_FAIL = "FAIL"
AUTH_ERROR = "AUTH_ERROR"


class BaseResponse(BaseModel):
    data: Any = None
    code: str
    message: str = ""


class ServiceResult(BaseResponse):
    success: bool


class SuccessResult(ServiceResult):
    code: str = CODE_SUCCESS
    success: bool = True


class ErrorResult(ServiceResult):
    code: str = CODE_ERROR
    success: bool = False


class ListDataSchema(BaseModel):
    list: List[Dict[str, Any]] = []
    total: int = 0


class ResponseCodeEnum(str, Enum):
    success = CODE_SUCCESS
    err = CODE_ERROR
    fail = CODE_FAIL


class ResponseModel(BaseResponse):
    code: ResponseCodeEnum


class ListResponseModel(ResponseModel):
    data: ListDataSchema


class JSONResponse(ORJSONResponse):
    @staticmethod
    def default(obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        if isinstance(obj, BaseModel):
            return obj.dict()
        raise TypeError

    def render(self, content: Any) -> bytes:
        assert orjson is not None, "must be installed to use ORJSONResponse"
        return orjson.dumps(
            content, option=orjson.OPT_SERIALIZE_DATACLASS, default=JSONResponse.default
        )


def common_response(message: str, code: str, data: Any = None) -> JSONResponse:
    """
    Common Response
    """
    return JSONResponse(
        BaseResponse(
            message=message,
            code=code,
            data=data,
        ),
        status_code=200,
    )


def validation_error_response(
    message: str = "params format error",
    code: str = CODE_PARAMS_ERROR,
) -> JSONResponse:
    """
    Server Error Response
    """
    return JSONResponse(BaseResponse(message=message, code=code), status_code=422)


def server_error_response(
    message: str = "server error", code: str = CODE_SERVER_ERROR
) -> JSONResponse:
    """
    Server Error Response
    """
    return JSONResponse(BaseResponse(message=message, code=code), status_code=200)


def success_response(
    message: str = "", code: str = CODE_SUCCESS, data: Any = None
) -> JSONResponse:
    """
    Success Response
    """
    return common_response(message=message, code=code, data=data)


def error_response(
    message: str, code: str = CODE_ERROR, data: Any = None
) -> JSONResponse:
    """
    Error Response
    """
    return common_response(message=message, code=code, data=data)
