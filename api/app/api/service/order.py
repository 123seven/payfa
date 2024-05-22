import base64
import datetime
import hashlib
import hmac
import random
import re
import urllib.parse
from decimal import Decimal

import requests
from fastapi import BackgroundTasks
from loguru import logger
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exception import ServiceException
from app.core.response import SuccessResult
from app.models.order import Order, ApiKey
from app.schemas.api.common import (
    CheckOrderSchema,
    CreateOrderSchema,
    NotifySchema,
    SignSchema,
)


class OrderServices:
    def __init__(self, session: Session, background_tasks: BackgroundTasks):
        self.session = session
        self.tasks = background_tasks

    @classmethod
    def _create_order_id(cls):
        current_date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        suffix = "".join(random.choice("0123456789") for _ in range(6))
        return current_date + suffix

    @classmethod
    def check_sign(cls, sign_data: SignSchema, api_key: ApiKey):
        logger.info("{data}", data=sign_data)
        # 按照键名排序并生成键值对列表
        pairs = [f"{k}={v}" for k, v in sorted(sign_data.dict().items()) if k != "sign"]
        # 将键值对列表用 & 符号连接起来
        signature_str = "".join(pairs)

        signature = hmac.new(
            api_key.sk.encode(),
            signature_str.encode(),
            hashlib.sha256,
        ).hexdigest()
        logger.info("{signature}", signature=signature)

        if signature != sign_data.sign:
            raise ServiceException(message="sign error")

    @classmethod
    def _parse_amount(cls, msg: str):
        pattern = r"(\d+\.\d{2})"
        match = re.search(pattern, msg)
        if match:
            return float(match.group(1))

    def get_api_key(self, ak: str):
        api_key = self.session.query(ApiKey).filter(ApiKey.ak == ak).first()
        if not api_key:
            raise ServiceException(message="api key not found")
        return api_key

    async def create(self, data: CreateOrderSchema):
        api_key = self.get_api_key(data.ak)
        self.check_sign(data, api_key)

        # 查询未支付、未超时、金额一致的订单
        expired_time = datetime.datetime.now() - datetime.timedelta(
            seconds=settings.ORDER_EXPIRED_SECOND
        )
        last_order: Order = (
            self.session.query(Order)
            .filter(
                Order.price == data.price,
                Order.status == 0,
                Order.create_time > expired_time,
            )
            .order_by(Order.id.desc())
            .first()
        )
        if last_order:
            data.price = last_order.price + Decimal(0.01)

        order = Order(
            order_number=self._create_order_id(),
            payment_method=data.payment_method.value,
            price=data.price,
            notify_url=data.notify_url,
            api_key_id=api_key.id,
        )
        self.session.add(order)
        self.session.commit()
        data = {
            **order.to_dict(),
            "pay_url": "",
        }

        return SuccessResult(data=data)

    async def status(self, data: CheckOrderSchema):
        order: Order = (
            self.session.query(Order)
            .filter(
                Order.order_number == data.order_number,
            )
            .first()
        )
        return SuccessResult(data=order)

    def check_wechat_msg(self, msg: str):
        if "微信支付" not in msg:
            return "error"

    def check_alipay_msg(self, msg: str):
        if "支付宝" not in msg:
            return "error"

    def notify_platform(self, order: Order, api_key: ApiKey):
        notify_data = {
            "ak": api_key.ak,
            "pay_id": order.order_number,
            "pay_type": order.payment_method,
            "price": float(order.price),
            "really_price": float(order.amount),
        }

        # 字典序排序拼接签名字符串
        sorted_keys = sorted(notify_data.keys())
        signature_str = "".join([f"{key}={notify_data[key]}" for key in sorted_keys])
        signature = hmac.new(
            api_key.sk.encode(), signature_str.encode(), hashlib.sha256
        ).hexdigest()
        notify_data.setdefault("sign", signature)

        def _notify():
            logger.info(
                "callback notify_url:{notify_url} data:{data}",
                notify_url=order.notify_url,
                data=notify_data,
            )
            resp = requests.post(order.notify_url, json=notify_data)
            logger.info("{resp}", resp=resp)

        self.tasks.add_task(_notify)

    @classmethod
    def check_app_sign(cls, sign_data: SignSchema, api_key: ApiKey):
        secret_enc = api_key.sk.encode("utf-8")
        string_to_sign = "{}\n{}".format(sign_data.timestamp, api_key.sk)
        string_to_sign_enc = string_to_sign.encode("utf-8")
        hmac_code = hmac.new(
            secret_enc,
            string_to_sign_enc,
            digestmod=hashlib.sha256,
        ).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        if sign != sign_data.sign:
            raise ServiceException(message="sign error")

    async def notify(self, data: NotifySchema):
        logger.info("notify data:{data}", data=data)
        api_key = self.get_api_key(data.ak)
        self.check_app_sign(data, api_key)
        if "到账" not in data.msg:
            return "error"
        amount = self._parse_amount(data.msg)
        if not amount:
            return "error"
        expired_time = datetime.datetime.now() - datetime.timedelta(
            seconds=settings.ORDER_EXPIRED_SECOND
        )
        order = (
            self.session.query(Order)
            .filter(
                Order.price == amount,
                Order.status == 0,
                Order.create_time > expired_time,
            )
            .first()
        )

        if not order:
            return "未找到对应订单"

        order.amount = amount
        order.pay_time = datetime.datetime.now()
        self.session.merge(order)
        self.session.commit()

        api_key = self.get_api_key(data.ak)
        self.notify_platform(order, api_key)
        return "success"
