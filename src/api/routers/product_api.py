from typing import List

from sqlalchemy.ext.asyncio import async_sessionmaker
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ...managers import ProductManager
from ..schemas import ProductCreateSchema, ProductUpdateSchema

def prod_router_init(session_maker: async_sessionmaker):
    api = ProductManager(session_maker)
    router = APIRouter(prefix="/api/v1", tags=['Product'])

    @router.patch("/product")       
    async def update_product(product: ProductUpdateSchema):
        try:
            result = await api.update_product(product)
            return {
                'ok': True,
                'result': result
            }
        except Exception as e:
            return JSONResponse(
                {
                    'ok': False,
                    'detail': str(e)
                },
                status_code=500
            )

    @router.post("/product")
    async def create_product(product: ProductCreateSchema):
        try:
            result = await api.create_product(product)
            return {
                'ok': True,
                'result': result
            }
        except Exception as e:
            return JSONResponse(
                {
                    'ok': False,
                    'detail': str(e)
                },
                status_code=500
            )
        
    @router.get("/product/{id}")
    async def get_product(id: int):
        try:
            result = await api.get_product(id)
            return {
                'ok': True,
                'result': result
            }
        except Exception as e:
            return JSONResponse(
                {
                    'ok': False,
                    'detail': str(e)
                },
                status_code=500
            )
            
    @router.delete("/product/{id}")
    async def delete_product(id: int):
        try:
            result, detail = await api.delete_product(id)
            return {
                'ok': result,
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
    
    @router.get("/productall")
    async def get_all_product():
        try:
            return {
                'ok': True,
                'result': await api.get_all_products()
            }
        except Exception as e:
            return JSONResponse(
                {
                    'ok': False,
                    'detail': str(e)
                },
                status_code=500
            )
    
    @router.post("/products")
    async def get_products(ids: List[int]):
        try: 
            print(ids)
            return {
                'ok': True,
                'result': await api.get_products(ids)
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