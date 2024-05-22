from datetime import datetime

from sqlalchemy import DECIMAL, Column, DateTime, Integer, String

from app.models.database import BaseModel


class Order(BaseModel):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, index=True, doc="订单号")
    payment_method = Column(Integer, default=0, doc="支付方式 1:微信 2:支付宝")
    status = Column(Integer, default=0, doc="状态 0:未支付 1:已支付 2:超时")
    price = Column(DECIMAL, nullable=False, doc="订单价格")
    amount = Column(DECIMAL, default=None, doc="订单价格(支付金额)")

    pay_time = Column(DateTime, default=None, doc="支付时间")
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, onupdate=datetime.now, default=datetime.now)

    notify_url = Column(String, index=True, doc="回调地址")
    api_key_id = Column(Integer, nullable=False, doc="api_key_id")


class ApiKey(BaseModel):
    __tablename__ = "api_key"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, doc="")
    # 用于标示用户
    ak = Column(String, index=True, nullable=False, doc="Access Key")
    # 用于加密认证字符串和用来验证认证字符串的密钥
    sk = Column(String, nullable=False, doc="Secret Key")
    remark = Column(String, default="", doc="备注")
