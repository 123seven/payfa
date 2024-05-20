from fastapi import APIRouter, Depends, Body
from fastapi.params import Query
from sqlalchemy.orm import Session

from app.api.depends.authentication import jwt_authentication
from app.api.service.admin import AdminServices, AdminLoginServices
from app.core.cbv import cbv
from app.models.admin import Admin
from app.models.database import get_session
from app.schemas.api.common import (
    AdminFiltersSchema,
    PaginatorBySchema,
    AdminModelSchema,
    AdminUpdateSchema,
)

router = APIRouter()
login_router = APIRouter()


@cbv(router)
class AdminViewApi:
    def __init__(
        self,
        session: Session = Depends(get_session),
        admin: Admin = Depends(jwt_authentication),
    ):
        self.service = AdminServices(session, admin)

    @router.get("/list", summary="获取admin列表")
    async def list(
        self,
        user_name: str = Query(None, description="account or nickname 模糊查询"),
        admin_type: str = Query(None, description="管理员类型过滤"),
        page: int = Query(1, description="page"),
        page_size: int = Query(15, description="page_size"),
    ):
        filters = AdminFiltersSchema(user_name=user_name, admin_type=admin_type)
        paginator = PaginatorBySchema(page=page, page_size=page_size)

        return await self.service.lists(filters, paginator)

    @router.get("/{admin_id}", summary="获取admin详情")
    async def detail(self, admin_id: int):
        return await self.service.detail(admin_id)

    @router.post("/add", summary="创建admin")
    async def create(
        self,
        create_data: AdminModelSchema = Body(...),
    ):
        return await self.service.create(create_data)

    @router.put("/{admin_id}/update", summary="更新admin")
    async def update(
        self,
        admin_id: int,
        update_data: AdminUpdateSchema = Body(...),
    ):
        return await self.service.update(admin_id, update_data)

    @router.put("/{admin_id}/enabled", summary="禁用admin")
    async def enabled(self, admin_id: int):
        return await self.service.enabled(admin_id)

    @router.delete("/{admin_id}/delete", summary="删除admin")
    async def delete(self, admin_id: int):
        return await self.service.delete(admin_id)


@login_router.post("/login", summary="管理员登录")
async def login(
    account: str = Body(..., title="账号"),
    password: str = Body(..., title="密码"),
    session: Session = Depends(get_session),
):
    service = AdminLoginServices(session)
    return await service.login(account, password)
