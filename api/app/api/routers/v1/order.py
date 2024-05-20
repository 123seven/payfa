from fastapi import APIRouter, BackgroundTasks, Depends, Request
from sqlalchemy.orm import Session

from app.api.service.order import OrderServices
from app.core.cbv import cbv
from app.core.response import ResponseModel
from app.models.database import get_session
from app.schemas.api.common import CheckOrderSchema, CreateOrderSchema, NotifySchema

router = APIRouter()


@cbv(router)
class OrderViewApi:
    def __init__(
        self,
        background_tasks: BackgroundTasks,
        session: Session = Depends(get_session),
    ):
        self.service = OrderServices(session, background_tasks)

    @router.post("/create", response_model=ResponseModel)
    async def create(self, data: CreateOrderSchema):
        return await self.service.create(data)

    @router.get("/check", response_model=ResponseModel)
    async def check(self, data: CheckOrderSchema):
        return await self.service.status(data)

    @router.post("/notify")
    async def notify(self, req: Request, data: NotifySchema):
        return await self.service.notify(data)
