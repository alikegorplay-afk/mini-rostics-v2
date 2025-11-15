"""Хранит роутеры"""
from typing import List

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from .product_api import prod_router_init
from .order_api import order_router_init

def create(session: async_sessionmaker[AsyncSession]) -> List[APIRouter]:
    return [
        prod_router_init(session),
        order_router_init(session)
    ]