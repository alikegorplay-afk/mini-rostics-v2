from typing import Literal

from sqlalchemy.ext.asyncio import async_sessionmaker
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ...core.database.models import OrderStatus
from ...managers import OrderManager
from ...schemas.order import OrderItemSchema, CreateOrderSchema

def order_router_init(session_maker: async_sessionmaker):
    api = OrderManager(session_maker)
    router = APIRouter(prefix="/api/v1", tags=['Order'])
    
    @router.post('/order')
    async def create_order(order: CreateOrderSchema):
        try:
            return {
                'ok': True,
                'result': await api.create_order(order)
            }
        except Exception as e:
            return JSONResponse(
                {
                    'ok': False,
                    'detail': str(e)
                },
                status_code=500
            )
    
    
    @router.get("/order/{id}")
    async def ger_order(id: int):
        try:
            return {
                'ok': True,
                'result': await api.get_order(id) 
            }
        except Exception as e:
            return JSONResponse(
                {
                    'ok': False,
                    'detail': str(e)
                },
                status_code=500
            )
            
    @router.delete('/order/{id}')
    async def delete_order(id: int):
        try:
            ok, detail = await api.delete_order(id)
            return {
                'ok': ok,
                'detail': detail
            }
        except Exception as e:
            return JSONResponse(
                {
                    'ok': False,
                    'detail': str(e)
                },
                status_code=500
            )
    
    
    @router.patch('/order/{id}')
    async def update_order(id: int, order: OrderItemSchema):
        try:
            data = await api.update_order(id, order)
            return {
                'ok': True,
                'result': data
            }
        except Exception as e:
            return JSONResponse(
                {
                    'ok': False,
                    'detail': str(e)
                },
                status_code=500
            )
            
    @router.patch('/ordstatupd/{id}')
    async def update_status(id: int, status: Literal["Оплачен", "Неоплаченный"] = "Оплачен"):
        if status == "Оплачен":
            new_status = OrderStatus.PAID
        elif status == "Неоплаченный":
            new_status = OrderStatus.UNPAID
        else:
            return JSONResponse(
                {
                    'ok': False,
                    'detail': f"Не возможный статус {status}"
                },
                status_code=400,
            )
        try:
            await api.update_status(id, status=new_status)
            return {
                'ok': True
            }
        except Exception as e:
            return JSONResponse(
                {
                    'ok': False,
                    'detail': str(e)
                },
                status_code=500
            )
            
    return router