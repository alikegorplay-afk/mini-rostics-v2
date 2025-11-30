from dataclasses import dataclass
from typing import List, Iterable
from enum import Enum

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Float, Text


__all__ = [
    "Product",
    "Order",
    "OrderItem"
]

class OrderStatus(Enum):
    PAID = "Оплачен"
    UNPAID = "Неоплаченный"


class Base(DeclarativeBase): ...


@dataclass
class Product(Base):
    """Класс для хранения продуктов"""
    __tablename__ = "product"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    poster: Mapped[str] = mapped_column(String(1024))
    price: Mapped[float] = mapped_column(Float())
    count: Mapped[int] = mapped_column(Integer())
    description: Mapped[str] = mapped_column(Text())
    
    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'poster': self.poster,
            'price': self.price,
            'count': self.count,
            'description': self.description  
        }


class Order(Base):
    """Класс для хранения заказов"""
    __tablename__ = "order"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order")
    status: Mapped[str] = mapped_column(String(32), default=OrderStatus.UNPAID.value)
    
    def as_dict(self):
        return {
            'id': self.id,  
            'items': [item.as_dict() for item in self.items]
        }
    
    def append(self, value: "OrderItem"):
        if not isinstance(value, OrderItem):
            raise TypeError(f"Неподдерживаемый тип {type(value).__name__}")
        self.items.append(value)
        
    def extend(self, values: Iterable["OrderItem"]):
        for value in values:
            self.append(value)
    
    def __repr__(self):
        return f"Order(id={self.id}, items={len(self.items)}, status='{self.status}')"
    
    def __iter__(self):
        return iter(self.items)    
    

class OrderItem(Base):
    """Класс для хранения данных о части заказа"""
    __tablename__ = "order_item"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    count: Mapped[int] = mapped_column(Integer()) 
    
    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship("Product")
    
    def __repr__(self):
        return f"OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, count={self.count})"
        
    def as_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'count': self.count,
        }