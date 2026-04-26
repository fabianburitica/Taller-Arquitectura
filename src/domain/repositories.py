from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Product, ChatMessage


class IProductRepository(ABC):
    """
    Interfaz para el repositorio de productos.
    Define las operaciones disponibles sin implementar cómo se hacen.
    """

    @abstractmethod
    def get_all(self) -> List[Product]:
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def get_by_category(self, category: str) -> List[Product]:
        pass

    @abstractmethod
    def search(self, query: str) -> List[Product]:
        pass

    @abstractmethod
    def save(self, product: Product) -> Product:
        pass

    @abstractmethod
    def update(self, product: Product) -> Product:
        pass


class IChatRepository(ABC):
    """
    Interfaz para el repositorio de mensajes del chat.
    """

    @abstractmethod
    def save_message(self, message: ChatMessage) -> ChatMessage:
        pass

    @abstractmethod
    def get_messages_by_session(self, session_id: str) -> List[ChatMessage]:
        pass

    @abstractmethod
    def delete_session(self, session_id: str) -> None:
        pass

class IProductRepository(ABC):
    """
    Interface que define el contrato para acceder a productos.
    """

    @abstractmethod
    def get_all(self) -> List[Product]:
        """
        Obtiene todos los productos
        """
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Obtiene un producto por ID
        Retorna None si no existe
        """
        pass

    @abstractmethod
    def get_by_brand(self, brand: str) -> List[Product]:
        """
        Obtiene productos de una marca específica
        """
        pass

    @abstractmethod
    def get_by_category(self, category: str) -> List[Product]:
        """
        Obtiene productos de una categoría específica
        """
        pass

    @abstractmethod
    def save(self, product: Product) -> Product:
        """
        Guarda o actualiza un producto
        """
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """
        Elimina un producto por ID
        Retorna True si se eliminó, False si no existía
        """
        pass

class IChatRepository(ABC):
    """
    Interface para gestionar el historial de conversaciones.
    Define las operaciones necesarias para almacenar y recuperar mensajes.
    """

    @abstractmethod
    def save_message(self, message: ChatMessage) -> ChatMessage:
        """
        Guarda un mensaje en el historial.
        Retorna el mensaje guardado con su ID asignado (si aplica).
        """
        pass

    @abstractmethod
    def get_session_history(
        self, session_id: str, limit: Optional[int] = None
    ) -> List[ChatMessage]:
        """
        Obtiene el historial completo de una sesión.

        - Si 'limit' está definido, retorna solo los últimos N mensajes.
        - Los mensajes deben estar en orden cronológico (más antiguos primero).
        """
        pass

    @abstractmethod
    def delete_session_history(self, session_id: str) -> int:
        """
        Elimina todo el historial de una sesión.

        Retorna la cantidad de mensajes eliminados.
        """
        pass

    @abstractmethod
    def get_recent_messages(self, session_id: str, count: int) -> List[ChatMessage]:
        """
        Obtiene los últimos N mensajes de una sesión.

        - Es clave para construir el contexto del chat.
        - Debe retornar en orden cronológico (más antiguos primero).
        """
        pass

class ProductNotFoundError(Exception):
    """
    Se lanza cuando se busca un producto que no existe.
    """

    def __init__(self, product_id: int = None):
        if product_id is not None:
            message = f"Producto con ID {product_id} no encontrado"
        else:
            message = "Producto no encontrado"
        super().__init__(message)


class InvalidProductDataError(Exception):
    """
    Se lanza cuando los datos de un producto son inválidos.
    """

    def __init__(self, message: str = "Datos de producto inválidos"):
        super().__init__(message)


class ChatServiceError(Exception):
    """
    Se lanza cuando hay un error en el servicio de chat.
    """

    def __init__(self, message: str = "Error en el servicio de chat"):
        super().__init__(message)