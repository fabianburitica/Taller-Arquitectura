class ChatServiceError(Exception):
    def __init__(self, message: str = "Error en el servicio de chat"):
        super().__init__(message)

"""
Excepciones específicas del dominio.
"""


class ProductNotFoundError(Exception):
    def __init__(self, product_id: int = None):
        if product_id:
            message = f"Producto con ID {product_id} no encontrado"
        else:
            message = "Producto no encontrado"
        super().__init__(message)


class InvalidProductDataError(Exception):
    def __init__(self, message: str = "Datos de producto inválidos"):
        super().__init__(message)


class ChatServiceError(Exception):
    def __init__(self, message: str = "Error en el servicio de chat"):
        super().__init__(message)