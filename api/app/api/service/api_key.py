import secrets
import string
import uuid

from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from app.core.response import SuccessResult, ErrorResult, ServiceResult, ListDataSchema
from app.models.order import ApiKey
from app.schemas.api.common import (
    ApiKeySchema,
    PaginatorBySchema,
    ApiKeyFiltersSchema,
    ApiKeyInfoSchema,
)
from app.tools.paginator import Paginator


class ApiKeyServices:
    def __init__(self, session: Session, background_tasks: BackgroundTasks):
        self.session = session
        self.tasks = background_tasks

    @classmethod
    def generate_access_key(cls):
        # 生成随机的AK
        return str(uuid.uuid4().hex)

    @classmethod
    def generate_secret_key(cls):
        # 生成随机的SK
        return "".join(
            secrets.choice(string.ascii_letters + string.digits) for _ in range(64)
        )

    async def list(
        self,
        filters: ApiKeyFiltersSchema,
        paginator: PaginatorBySchema,
    ) -> SuccessResult:
        query = self.session.query(ApiKey).order_by(ApiKey.id)

        if filters.name:
            query = query.filter(
                ApiKey.name.ilike("%" + filters.name + "%"),
            )

        pag = Paginator(query, paginator.page_size)
        page_query = pag.get_page_query(paginator.page)
        result = [ApiKeyInfoSchema.from_orm(item).dict() for item in page_query.all()]
        return SuccessResult(data=ListDataSchema(list=result, total=pag.total))

    async def create(self, data: ApiKeySchema) -> ServiceResult:
        if self.session.query(ApiKey).filter(ApiKey.name == data.name).first():
            return ErrorResult(message="api_key name already exists")

        api_key = ApiKey(
            name=data.name,
            ak=self.generate_access_key(),
            sk=self.generate_secret_key(),
            remark=data.remark,
        )

        self.session.add(api_key)
        self.session.commit()
        return SuccessResult(data=api_key.to_dict())

    async def update(self, api_key_id: int, data: ApiKeySchema) -> ServiceResult:
        api_key = self.session.query(ApiKey).filter(ApiKey.id == api_key_id).first()
        if not api_key:
            return ErrorResult(message="api_key not found")
        api_key.name = data.name
        api_key.remark = data.remark
        self.session.commit()
        return SuccessResult(data=ApiKeyInfoSchema.from_orm(api_key).dict())

    async def delete(self, api_key_id: int) -> ServiceResult:
        api_key = self.session.query(ApiKey).filter(ApiKey.id == api_key_id).first()
        if not api_key:
            return ErrorResult(message="api_key not found")

        self.session.delete(api_key)
        self.session.commit()
        return SuccessResult()
