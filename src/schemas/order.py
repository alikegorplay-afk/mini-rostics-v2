from typing import Optional, List
from pydantic import BaseModel, field_validator, ConfigDict, model_validator


class OrderItemSchema(BaseModel):
    """Схема для обозночение продукта"""
    product_id: int
    count: int


class CreateOrderSchema(BaseModel):
    """Схема для создание заказа"""
    items: List[OrderItemSchema]
    
    
class OrderItemResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    product_id: int
    count: int

class OrderSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    status: str
    items: List[OrderItemResponseSchema]