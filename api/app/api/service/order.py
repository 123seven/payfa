import datetime
import random
import re

from fastapi import BackgroundTasks
from loguru import logger
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.response import SuccessResult
from app.models.order import Order
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
    def check_sign(cls, sign_data: SignSchema):
        print("data:", sign_data)
        logger.error(
            "{data}",
            data=sign_data
        )
        # 按照键名排序并生成键值对列表
        pairs = [f"{k}={v}" for k, v in sorted(sign_data.dict().items()) if k != "sign"]

        # 将键值对列表用 & 符号连接起来
        _string = "".join(pairs)

    @classmethod
    def _parse_amount(cls, msg: str):
        pattern = r"(\d+\.\d{2})元"
        match = re.search(pattern, msg)
        if match:
            return float(match.group(1))

    async def create(self, data: CreateOrderSchema):
        self.check_sign(data)
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
            data.price = last_order.price + 0.01

        order = Order(
            order_number=self._create_order_id(),
            payment_method=data.payment_method.value,
            price=data.price,
        )
        self.session.add(order)
        self.session.commit()
        return SuccessResult(data=order)

    async def status(self, data: CheckOrderSchema):
        order: Order = (
            self.session.query(Order)
            .filter(
                Order.order_number == data.order_number,
            )
            .first()
        )
        return SuccessResult(data=order)

    async def notify(self, data: NotifySchema):
        self.check_sign(data)
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
        return "success"
