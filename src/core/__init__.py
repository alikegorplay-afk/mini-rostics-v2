"""Ядро системы"""
__version__ = 0.1

from .database.models import Product, Order, OrderItem
from .const import DATA_BASE_NAME, PATH_TO_DATABASE, PATH_TO_SAVE_IMAGE, DATABASE_URL

from .config import config

__all__ = [
    "Product",
    "Order",
    "OrderItem",
    "DATA_BASE_NAME",
    "PATH_TO_DATABASE",
    "PATH_TO_SAVE_IMAGE",
    "DATABASE_URL",
    "config"
]