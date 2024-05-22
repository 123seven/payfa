from fastapi import APIRouter, BackgroundTasks, Depends, Query
from sqlalchemy.orm import Session

from app.api.service.api_key import ApiKeyServices
from app.core.cbv import cbv
from app.core.response import ResponseModel
from app.models.database import get_session
from app.schemas.api.common import (
    ApiKeySchema,
    AdminFiltersSchema,
    PaginatorBySchema,
    ApiKeyFiltersSchema,
)

router = APIRouter()


@cbv(router)
class OrderViewApi:
    def __init__(
        self,
        background_tasks: BackgroundTasks,
        session: Session = Depends(get_session),
    ):
        self.service = ApiKeyServices(session, background_tasks)

    @router.get("/list", response_model=ResponseModel)
    async def list(
        self,
        name: str = Query(None, description="name 模糊查询"),
        page: int = Query(1, description="page"),
        page_size: int = Query(15, description="page_size"),
    ):
        filters = ApiKeyFiltersSchema(name=name)
        paginator = PaginatorBySchema(page=page, page_size=page_size)

        return await self.service.list(filters, paginator)

    @router.post("/create", response_model=ResponseModel)
    async def create(self, data: ApiKeySchema):
        return await self.service.create(data)

    @router.post("{api_key_id}/update/", response_model=ResponseModel)
    async def update(self, api_key_id: int, data: ApiKeySchema):
        return await self.service.update(api_key_id, data)

    @router.post("{api_key_id}/delete/", response_model=ResponseModel)
    async def delete(self, api_key_id: int):
        return await self.service.delete(api_key_id)
