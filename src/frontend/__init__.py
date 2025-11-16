import os

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi import HTTPException

from ..core.const import PATH_TO_SAVE_IMAGE


def get_router(session: async_sessionmaker[AsyncSession]):
    from ..managers import ProductManager
    api = ProductManager(session)
    router = APIRouter()

    # Получаем абсолютный путь к директории frontend
    FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMPLATES_DIR = os.path.join(FRONTEND_DIR, "templates")
    STATIC_DIR = os.path.join(FRONTEND_DIR, "static")

    
    # Настройка шаблонов
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

    @router.get("/about", response_class=HTMLResponse)
    async def about(request: Request):
        return templates.TemplateResponse("about.html", {"request": request})

    @router.get("/contact", response_class=HTMLResponse)
    async def contact(request: Request):
        return templates.TemplateResponse("contact.html", {"request": request})
    
    @router.get("/data/img/{poster}", response_class=FileResponse)
    async def get_poster(poster: str):
        image_path = PATH_TO_SAVE_IMAGE / poster
        
        if not image_path.exists():
            raise HTTPException(status_code=404, detail="Image not found")
        
        return FileResponse(image_path)
    
    return router