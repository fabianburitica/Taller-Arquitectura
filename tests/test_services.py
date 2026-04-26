import pytest
from src.application.chat_service import ChatService
from src.application.dtos import ChatMessageRequestDTO


#  Mock de repositorio de productos
class FakeProductRepo:
    def get_all(self):
        return []


#  Mock de repositorio de chat
class FakeChatRepo:
    def __init__(self):
        self.messages = []

    def get_recent_messages(self, session_id, count):
        return []

    def save_message(self, message):
        self.messages.append(message)
        return message


#  Mock de IA
class FakeAIService:
    async def generate_response(self, user_message, products, context):
        return "Respuesta fake de IA"


# =========================
# TEST CHAT SERVICE
# =========================

@pytest.mark.asyncio
async def test_process_message():
    service = ChatService(
        product_repository=FakeProductRepo(),
        chat_repository=FakeChatRepo(),
        ai_service=FakeAIService()
    )

    request = ChatMessageRequestDTO(
        session_id="test123",
        message="Hola"
    )

    response = await service.process_message(request)

    assert response.session_id == "test123"
    assert response.user_message == "Hola"
    assert "Respuesta fake" in response.assistant_message