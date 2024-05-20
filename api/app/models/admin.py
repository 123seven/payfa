from datetime import datetime

from passlib.context import CryptContext
from sqlalchemy import DECIMAL, Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import Session

from app.models.database import BaseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Admin(BaseModel):
    """
    管理员用户表
    """

    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, index=True)

    account = Column(String(32),  nullable=False, doc="管理员账号")
    password = Column(String(128), nullable=False, doc="密码")

    nickname = Column(String(32), nullable=True, doc="管理员昵称")
    avatar_url = Column(String(255), nullable=True, doc="头像URL")
    wechat_id = Column(String(32), nullable=True, doc="微信号")
    real_name = Column(String(32), nullable=True, doc="真实姓名")
    email = Column(String(32), nullable=True, doc="邮箱")
    mobile = Column(String(30), nullable=True, doc="手机号码")

    enabled = Column(Boolean, default=True, doc="启用")
    delete = Column(Boolean, default=False, doc="删除")
    type = Column(Integer, default=1, doc="管理员类型0:超级管理员1:管理员")
    last_at = Column(DateTime, nullable=True, doc="最后登录时间")
    remark = Column(String(255), nullable=True, doc="备注")

    class Meta:
        exclude = ("password",)

    def set_password(self, password: str):
        """设置加密密码
        :param password: 明文密码
        """
        self.password = pwd_context.hash(password)

    def check_password(self, raw_password: str) -> bool:
        """检查密码是否正确
        :param raw_password: 明文密码
        :return: bool
        """
        return pwd_context.verify(raw_password, self.password)

    @staticmethod
    def create_super_admin(
        account: str = "super_admin", password: str = "1qaz2wsx#EDC"
    ) -> "Admin":
        """创建超级管理员
        :param account: str 管理员账号
        :param password: str 密码
        :return: admin obj
        """
        from database import engine

        with Session(engine) as session:
            instance = (
                session.query(Admin)
                .filter(Admin.account == account, Admin.type == 0)
                .first()
            )
            if not instance:
                instance = Admin(account=account, type=0, password="0")
                instance.set_password(password)
                session.add(instance)

            session.merge(instance)
            session.commit()
            return instance
