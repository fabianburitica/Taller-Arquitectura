from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Product:
    """
    Entidad que representa un producto en el e-commerce.
    Contiene la lógica de negocio relacionada con productos.
    """
    id: Optional[int]
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    def __post_init__(self):
        """
        Validaciones después de crear el objeto
        """
        if self.price <= 0:
            raise ValueError("El precio debe ser mayor a 0")

        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo")

        if not self.name or self.name.strip() == "":
            raise ValueError("El nombre del producto no puede estar vacío")

    def is_available(self) -> bool:
        """
        Retorna True si hay stock disponible
        """
        return self.stock > 0

    def reduce_stock(self, quantity: int) -> None:
        """
        Reduce el stock del producto
        """
        if quantity <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")

        if quantity > self.stock:
            raise ValueError("No hay suficiente stock disponible")

        self.stock -= quantity

    def increase_stock(self, quantity: int) -> None:
        """
        Aumenta el stock del producto
        """
        if quantity <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")

        self.stock += quantity


@dataclass
class ChatMessage:
    """
    Entidad que representa un mensaje en el chat.
    """
    id: Optional[int]
    session_id: str
    role: str  # 'user' o 'assistant'
    message: str
    timestamp: datetime

    def __post_init__(self):
        """
        Validaciones del mensaje
        """
        if self.role not in ["user", "assistant"]:
            raise ValueError("El rol debe ser 'user' o 'assistant'")

        if not self.message or self.message.strip() == "":
            raise ValueError("El mensaje no puede estar vacío")

        if not self.session_id or self.session_id.strip() == "":
            raise ValueError("El session_id no puede estar vacío")

    def is_from_user(self) -> bool:
        """
        Retorna True si el mensaje es del usuario
        """
        return self.role == "user"

    def is_from_assistant(self) -> bool:
        """
        Retorna True si el mensaje es del asistente
        """
        return self.role == "assistant"
    

@dataclass
class ChatContext:
    """
    Value Object que encapsula el contexto de una conversación.
    Mantiene los mensajes recientes para dar coherencia al chat.
    """
    messages: list[ChatMessage]
    max_messages: int = 6

    def get_recent_messages(self) -> list[ChatMessage]:
        """
        Retorna los últimos N mensajes
        """
        return self.messages[-self.max_messages:]

    def format_for_prompt(self) -> str:
        """
        Formatea los mensajes para el prompt de la IA
        """
        formatted_messages = []

        for msg in self.get_recent_messages():
            if msg.is_from_user():
                formatted_messages.append(f"Usuario: {msg.message}")
            elif msg.is_from_assistant():
                formatted_messages.append(f"Asistente: {msg.message}")

        return "\n".join(formatted_messages)