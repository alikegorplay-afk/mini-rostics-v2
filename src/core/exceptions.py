class ProductError(Exception):
    """Базовая ошибка для обозночение проблем с продуктом"""
    
class ProductNotFoundError(ProductError):
    """Ошибка обозночающая что продукт не найден"""
    
class OrderError(Exception):
    """Базовый класс для обазночение проблем с заказом"""
    
class OrderNotFoundError(OrderError):
    """Ошибка обозночающая что заказ не найден"""