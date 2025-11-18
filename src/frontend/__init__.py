import os

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from ..core.const import PATH_TO_SAVE_IMAGE


def get_router(session: async_sessionmaker[AsyncSession]):
    from ..managers import ProductManager
    from ..managers import OrderManager
    
    api = ProductManager(session)
    ord_api = OrderManager(session)
    router = APIRouter()

    # Получаем абсолютный путь к директории frontend
    FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMPLATES_DIR = os.path.join(FRONTEND_DIR, "templates")
    
    templates = Jinja2Templates(directory=TEMPLATES_DIR)

    @router.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    @router.get("/catalog", response_class=HTMLResponse)
    async def catalog(request: Request):
        products = await api.get_all_products()
        return templates.TemplateResponse("catalog.html", {
                                            "request": request,
                                            "products": [x.model_dump() for x in products]
                                        }
                                        )

    @router.get("/order/{id}", response_class=HTMLResponse)
    async def about(id: int, request: Request):
        data = await ord_api.get_order(id)
        
        if not data:
            return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
        else:
            # Получаем продукты для всех items в заказе
            product_ids = [x.product_id for x in data.items]
            products_list = await api.get_products(product_ids)
            products = {x.id: x for x in products_list}
            result = 0
            
            items = []
            for order_item in data.items:
                product = products.get(order_item.product_id)
                if product:
                    result += order_item.count * product.price
                    items.append(
                        {
                            'title': product.title,
                            'poster': product.poster if product.poster.startswith('http') else "/" + product.poster,
                            'price': product.price,
                            'count': order_item.count
                        }
                    )
                    
            # Используем более уникальное имя переменной
            order_info = {
                'status': data.status,
                'id': data.id,
                'sum': result,
                'data': items
            }
            
            return templates.TemplateResponse("order.html", 
                                            {
                                                "request": request, 
                                                'order_info': order_info,  # Изменили на order_info
                                            }
                                        )
    
    @router.get("/data/img/{poster}", response_class=FileResponse)
    async def get_poster(poster: str):
        image_path = PATH_TO_SAVE_IMAGE / poster
        
        if not image_path.exists():
            raise HTTPException(status_code=404, detail="Image not found")
        
        return FileResponse(image_path)
    
    return router