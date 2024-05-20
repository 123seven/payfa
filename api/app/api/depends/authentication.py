# @Time    : 2023/3/21 9:43 PM
# @Author  : seven
# @File    : authentication.py
# @Desc    :
import datetime

import jwt
from fastapi import Depends, Header
from jwt import DecodeError, ExpiredSignatureError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exception import ServiceException
from app.core.response import AUTH_ERROR
from app.models.admin import Admin
from app.models.database import get_session


def token_check(token: str, session: Session) -> Admin:
    try:
        token_without_bearer = token.split(" ")[1]  # 去除 Bearer 字段
        user = get_token_data(token_without_bearer)
        if not user["user_id"]:
            raise ServiceException("账号不存在", AUTH_ERROR)
        instance = session.get(Admin, user["user_id"])
        if not instance:
            raise ServiceException("账号不存在", AUTH_ERROR)

        if instance.delete:
            raise ServiceException(403, "账号不存在")
        if instance.enabled is False:
            raise ServiceException(200, "账号已被禁用，请联系管理员")
        return instance
    except (KeyError, TypeError, IndexError, DecodeError, ExpiredSignatureError):
        raise ServiceException("TOKEN错误或不存在", AUTH_ERROR)


def jwt_authentication(
    token: str = Header(None, description="token", alias="Authorization"),
    session: Session = Depends(get_session),
) -> Admin:
    if token:
        return token_check(token, session)
    else:
        raise ServiceException("TOKEN不存在", AUTH_ERROR)


def get_token(
    user_pk: int, _type: str = "admin", expiration: int = 60 * 60 * 24 * 5
) -> str:
    """
    获取token
    :param user_pk: 用户主键
    :param _type: 用户类型 admin or user
    :param expiration: 过期时间，默认5天
    :return: jwt token str
    """
    expire = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration)
    to_encode = {"user_id": user_pk, "type": _type, "exp": expire}
    return jwt.encode(
        to_encode, settings.JWT_SECRET_KEY + _type, algorithm=settings.JWT_ALGORITHM
    )


def get_token_data(token: str, _type: str = "admin") -> dict:
    """
    token返回data
    :param token: jwt token
    :param _type: 用户类型 admin or user
    :return: data dict
    """
    return jwt.decode(
        token, settings.JWT_SECRET_KEY + _type, algorithms=[settings.JWT_ALGORITHM]
    )


def set_data(data: dict, expiration: int = 7200) -> str:
    """加密一个dict数据"""
    expire = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration)
    to_encode = {"exp": expire}
    to_encode.update(**data)
    return jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


def get_data(key: str) -> dict:
    """解密一个key"""
    return jwt.decode(key, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])


__all__ = [
    "get_token",
    "get_token_data",
    "jwt_authentication",
    "set_data",
    "get_data",
]
