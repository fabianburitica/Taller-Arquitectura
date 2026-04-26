from typing import List, Optional
from datetime import datetime
from src.domain.entities import Product, ChatMessage, ChatContext
from src.domain.repositories import IProductRepository, IChatRepository
from src.domain.exceptions import ProductNotFoundError, InvalidProductDataError, ChatServiceError
from src.application.dtos import (
    ChatMessageRequestDTO,
    ChatMessageResponseDTO,
    ChatHistoryDTO,
    ProductDTO,
)

class ChatService:
    def __init__(
        self,
        product_repository: IProductRepository,
        chat_repository: IChatRepository,
        ai_service,
    ):
        self.product_repository = product_repository
        self.chat_repository = chat_repository
        self.ai_service = ai_service

    async def process_message(
        self, request: ChatMessageRequestDTO
    ) -> ChatMessageResponseDTO:
        try:
            # 1. Obtener productos
            products = self.product_repository.get_all()

            # 2. Obtener historial reciente
            history = self.chat_repository.get_recent_messages(
                request.session_id, count=6
            )

            # 3. Crear contexto
            context = ChatContext(messages=history)

            # 4. Llamar a la IA (puede ser mock por ahora)
            assistant_response = await self.ai_service.generate_response(
                user_message=request.message,
                products=products,
                context=context,
            )

            # 5. Guardar mensaje del usuario
            user_msg = ChatMessage(
                id=None,
                session_id=request.session_id,
                role="user",
                message=request.message,
                timestamp=datetime.utcnow(),
            )
            self.chat_repository.save_message(user_msg)

            # 6. Guardar respuesta del asistente
            assistant_msg = ChatMessage(
                id=None,
                session_id=request.session_id,
                role="assistant",
                message=assistant_response,
                timestamp=datetime.utcnow(),
            )
            self.chat_repository.save_message(assistant_msg)

            # 7. Retornar respuesta
            return ChatMessageResponseDTO(
                session_id=request.session_id,
                user_message=request.message,
                assistant_message=assistant_response,
                timestamp=datetime.utcnow(),
            )

        except Exception as e:
            raise ChatServiceError(f"Error procesando mensaje: {str(e)}")

    def get_session_history(
        self, session_id: str, limit: Optional[int] = None
    ) -> List[ChatHistoryDTO]:
        messages = self.chat_repository.get_session_history(session_id, limit)

        return [
            ChatHistoryDTO(
                id=m.id,
                role=m.role,
                message=m.message,
                timestamp=m.timestamp,
            )
            for m in messages
        ]

    def clear_session_history(self, session_id: str) -> int:
        return self.chat_repository.delete_session_history(session_id)