from fastapi import APIRouter

from . import admin as router_admin
from .order import router as order_router

v1_router = APIRouter()

v1_router.include_router(router_admin.login_router, prefix="/admin", tags=["admin"])
v1_router.include_router(
    router_admin.router,
    prefix="/admin",
    tags=["admin"],
)

v1_router.include_router(
    order_router,
    prefix="/order",
    tags=["order"],
)
