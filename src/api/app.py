import os

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from .routers import create


def create_app(sessionmaker: async_sessionmaker[AsyncSession]) -> FastAPI:
    app = FastAPI()
    for router in create(sessionmaker):
        app.include_router(router)

    TEMPLATES_DIR = os.path.join("src/frontend/", "templates")
    templates = Jinja2Templates(directory=TEMPLATES_DIR)
    
    @app.exception_handler(404)
    async def not_found_exception_handler(request: Request, exc: HTTPException):
        return templates.TemplateResponse(
            "404.html",
            {"request": request},
            status_code=404
        )

    return app