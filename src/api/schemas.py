from typing import Optional, List
from pydantic import BaseModel, field_validator, ConfigDict, model_validator


class Validator:
    @staticmethod
    def validate_title(value: str) -> str:
        """Валидация названия"""
        value = value.strip()
        if not value:
            raise ValueError("Название не может быть пустым")
        if len(value) > 255:
            raise ValueError("Название слишком длинное")
        return value
    
    @staticmethod
    def validate_price(value: float) -> float:
        """Валидация цены"""
        if value < 0:
            raise ValueError("Цена не может быть отрицательной")
        if value > 1_000_000:
            raise ValueError("Цена слишком высокая")
        return round(value, 2)
    
    @staticmethod
    def validate_count(value: int) -> int:
        """Валидация количества"""
        if value < 0:
            raise ValueError("Количество не может быть отрицательным")
        if value > 100_000:
            raise ValueError("Количество слишком большое")
        return value
    
    @staticmethod
    def validate_poster(value: str) -> str:
        """Валидация постера"""
        if value and len(value) > 1024:
            raise ValueError("Ссылка на постер слишком длинная")
        return value


class ProductBaseSchema(BaseModel):
    """Базовая схема с общими валидациями"""
    model_config = ConfigDict(from_attributes=True)
    
    title: str
    poster: str
    price: float
    count: int
    description: str
    
    @field_validator('title')
    def validate_title(cls, value: str) -> str:
        return Validator.validate_title(value)
    
    @field_validator('price')
    def validate_price(cls, value: float) -> float:
        return Validator.validate_price(value)
    
    @field_validator('count')
    def validate_count(cls, value: int) -> int:
        return Validator.validate_count(value)
    
    @field_validator('poster')
    def validate_poster(cls, value: str) -> str:
        return Validator.validate_poster(value)


class ProductSchema(ProductBaseSchema):
    """Схема для чтения продукта (с ID)"""
    id: int


class ProductCreateSchema(ProductBaseSchema):
    """Схема для создания продукта (без ID)"""
    pass


class ProductUpdateSchema(BaseModel):
    """Схема для обновления продукта"""
    model_config = ConfigDict(from_attributes=True)
    id: int
    
    title: Optional[str] = None
    poster: Optional[str] = None
    price: Optional[float] = None
    count: Optional[int] = None
    description: Optional[str] = None
    
    @field_validator('title')
    def validate_optional_title(cls, value: Optional[str]) -> Optional[str]:
        """Валидация опционального названия"""
        if value is not None:
            return Validator.validate_title(value)
        return value

    @field_validator('poster', 'description')
    def validate_optional_strings(cls, value: Optional[str]) -> Optional[str]:
        """Валидация опциональных строк"""
        if value is not None and len(value) > 1024:
            raise ValueError("Значение слишком длинное")
        return value
    
    @field_validator('price')
    def validate_optional_price(cls, value: Optional[float]) -> Optional[float]:
        """Валидация опциональной цены"""
        if value is not None:
            return Validator.validate_price(value)
        return value
    
    @field_validator('count')
    def validate_optional_count(cls, value: Optional[int]) -> Optional[int]:
        """Валидация опционального количества"""
        if value is not None:
            return Validator.validate_count(value)
        return value
    
    @model_validator(mode='after')
    def validate_at_least_one_field(self):
        """Проверка, что хотя бы одно поле передано"""
        if all(value is None for value in self.model_dump().values()):
            raise ValueError("Хотя бы одно поле должно быть указано для обновления")
        return self
    

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