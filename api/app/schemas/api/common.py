import datetime
from enum import IntEnum
from typing import Optional

from pydantic import BaseModel, Field


# __all__ = [
#     "PaginatorBySchema",
#     "PaymentMethod",
#     "SignSchema",
#     "CreateOrderSchema",
#     "CheckOrderSchema",
#     "NotifySchema",
# ]


class PaginatorBySchema(BaseModel):
    page: int = Field(default=1, ge=0)
    page_size: int = Field(default=20, ge=0, le=100)


class PaymentMethod(IntEnum):
    WECHAT_PAY = 1
    ALI_PAY = 1


class SignSchema(BaseModel):
    ak: str
    sign: str


class CreateOrderSchema(SignSchema):
    price: float
    payment_method: PaymentMethod = Field(default=PaymentMethod.WECHAT_PAY)
    notify_url: str


class CheckOrderSchema(SignSchema):
    order_number: str


class NotifySchema(SignSchema):
    msg: str


class AdminFiltersSchema(BaseModel):
    user_name: Optional[str]
    admin_type: Optional[int]


class AdminModelSchema(BaseModel):
    account: str = Field(max_length=32, description="管理员账号")
    password: str = Field(max_length=128, description="密码")
    nickname: str = Field(None, max_length=32, null=True, description="管理员昵称")
    avatar_url: str = Field(None, max_length=255, null=True, description="头像URL")
    mobile: str = Field(None, max_length=30, null=True, description="手机号码")
    email: str = Field(None, max_length=32, null=True, description="邮箱")
    remark: str = Field(None, max_length=255, null=True, description="备注")


class AdminUpdateSchema(BaseModel):
    password: str = Field(None, max_length=128, null=True, description="密码")
    nickname: str = Field(None, max_length=32, null=True, description="管理员昵称")
    avatar_url: str = Field(None, max_length=255, null=True, description="头像URL")
    remark: str = Field(None, max_length=255, null=True, description="备注")
    mobile: str = Field(None, max_length=30, null=True, description="手机号码")
    email: str = Field(None, max_length=32, null=True, description="邮箱")


class AdminInfoSchema(BaseModel):
    id: int
    account: str = Field(max_length=32, description="管理员账号")
    nickname: str = Field(None, max_length=32, null=True, description="管理员昵称")
    avatar_url: str = Field(None, max_length=255, null=True, description="头像URL")
    mobile: str = Field(None, max_length=30, null=True, description="手机号码")
    email: str = Field(None, max_length=32, null=True, description="邮箱")
    last_at: datetime.datetime = Field(None, doc="最后登录时间")
    created_at: datetime.datetime = Field(None, doc="创建时间")
    updated_at: datetime.datetime = Field(None, doc="更新时间")

    class Config:
        orm_mode = True
