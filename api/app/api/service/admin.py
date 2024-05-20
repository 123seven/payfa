import datetime

from loguru import logger
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.api.depends.authentication import get_token
from app.core.exception import ServiceException
from app.core.response import ErrorResult, SuccessResult, ListDataSchema
from app.models.admin import Admin
from app.schemas.api.common import (
    AdminFiltersSchema,
    AdminInfoSchema,
    AdminModelSchema,
    AdminUpdateSchema,
    PaginatorBySchema,
)
from app.tools.paginator import Paginator


class AdminServices:
    def __init__(self, session: Session, admin: Admin):
        self.session = session
        self.admin = admin

    def check_admin_by_id(self, admin_id: int) -> Admin:
        instance = (
            self.session.query(Admin)
            .filter(Admin.id == admin_id, Admin.delete == False)
            .first()
        )
        if not instance:
            raise ServiceException(message="账号不存在")
        return instance

    def check_account_exists(self, account):
        instance = (
            self.session.query(Admin)
            .filter(Admin.account == account, Admin.delete == False)
            .first()
        )
        if instance:
            raise ServiceException(message="账号已存在")

    async def lists(self, filters: AdminFiltersSchema, paginator: PaginatorBySchema):
        query = (
            self.session.query(
                Admin.id,
                Admin.account,
                Admin.nickname,
                Admin.avatar_url,
                Admin.email,
                Admin.type,
                Admin.enabled,
                Admin.last_at,
                Admin.created_at,
                Admin.updated_at,
            )
            .filter(Admin.delete == False)
            .order_by(Admin.id)
        )
        if filters.user_name:
            query = query.filter(
                or_(
                    Admin.account.ilike("%" + filters.user_name + "%"),
                    Admin.nickname.ilike("%" + filters.user_name + "%"),
                )
            )

        if filters.admin_type is not None:
            query = query.filter(Admin.type == filters.admin_type)
        pag = Paginator(query, paginator.page_size)
        page_query = pag.get_page_query(paginator.page)
        result = [AdminInfoSchema.from_orm(item).dict() for item in page_query.all()]
        return ListDataSchema(list=result, total=pag.total)

    async def create(self, create_data: AdminModelSchema):
        if self.admin.type != 0:
            raise ServiceException(message="权限不足，无法创建管理员账号")
        self.check_account_exists(create_data.account)

        data = create_data.dict(exclude_unset=True)
        data.setdefault("type", 1)

        instance = Admin(**data)
        instance.set_password(create_data.password)
        self.session.add(instance)
        self.session.merge(instance)
        self.session.commit()

        return SuccessResult(data=AdminInfoSchema.from_orm(instance).dict())

    async def detail(self, admin_id: int):
        instance = self.check_admin_by_id(admin_id)
        return SuccessResult(data=AdminInfoSchema.from_orm(instance).dict())

    async def enabled(self, admin_id: int):
        instance = self.check_admin_by_id(admin_id)
        if self.admin.type != 0:
            return ErrorResult(message="权限不够，超级管理员才能禁用")
        if self.admin.id == instance.id:
            return ErrorResult(message="不能禁用当前账号")

        instance.enabled = not instance.enabled
        self.session.merge(instance)
        self.session.commit()
        return SuccessResult()

    async def update(self, admin_id: int, update_data: AdminUpdateSchema):
        instance = self.check_admin_by_id(admin_id)
        if self.admin.type != 0:
            if self.admin.id != instance.id:
                return ErrorResult(message="权限不够，不能修改他人账号信息")

        data = update_data.dict(exclude_unset=True)
        instance.__dict__.update(**data)
        if data.get("password"):
            instance.set_password(data.get("password"))

        self.session.merge(instance)
        self.session.commit()

        return SuccessResult(data=AdminInfoSchema.from_orm(instance).dict())

    async def delete(self, admin_id: int):
        if self.admin.type != 0:
            return ErrorResult(message="权限不够，无法删除管理员账号")
        instance = self.check_admin_by_id(admin_id)
        if instance.type == 0:
            return ErrorResult(message="无法删除超级管理员")
        instance.delete = True
        self.session.merge(instance)
        self.session.commit()
        return SuccessResult()


class AdminLoginServices:
    def __init__(self, session: Session):
        self.session = session

    def check_admin_by_account(self, account: str) -> Admin:
        instance = (
            self.session.query(Admin)
            .filter(Admin.account == account, Admin.delete == False)
            .first()
        )
        if not instance:
            raise ServiceException(message="账号不存在")
        return instance

    async def login(self, account: str, password: str):
        instance = self.check_admin_by_account(account)
        if instance.enabled is not True:
            raise ServiceException(message="账号已经被禁用，请联系超级管理员")
        try:
            if not instance.check_password(password):
                raise ServiceException(message="密码错误，请检查")
        except Exception as e:
            logger.error(e)
            raise ServiceException(message="密码错误，请检查")
        instance.last_at = datetime.datetime.now()
        self.session.merge(instance)
        self.session.commit()

        data = AdminInfoSchema.from_orm(instance).dict()
        data.setdefault("token", get_token(instance.id))
        return SuccessResult(data=data)
