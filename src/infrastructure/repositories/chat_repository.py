from sqlalchemy.orm import Session
from typing import List, Optional

from src.domain.entities import ChatMessage
from src.domain.repositories import IChatRepository
from src.infrastructure.db.models import ChatMemoryModel


class SQLChatRepository(IChatRepository):
    def __init__(self, db: Session):
        self.db = db

    def save_message(self, message: ChatMessage) -> ChatMessage:
        model = self._entity_to_model(message)

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return self._model_to_entity(model)

    def get_session_history(
        self, session_id: str, limit: Optional[int] = None
    ) -> List[ChatMessage]:

        query = self.db.query(ChatMemoryModel).filter(
            ChatMemoryModel.session_id == session_id
        ).order_by(ChatMemoryModel.timestamp.asc())

        if limit:
            query = query.limit(limit)

        models = query.all()
        return [self._model_to_entity(m) for m in models]

    def delete_session_history(self, session_id: str) -> int:
        count = self.db.query(ChatMemoryModel).filter(
            ChatMemoryModel.session_id == session_id
        ).count()

        self.db.query(ChatMemoryModel).filter(
            ChatMemoryModel.session_id == session_id
        ).delete()

        self.db.commit()
        return count

    def get_recent_messages(self, session_id: str, count: int) -> List[ChatMessage]:
        models = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .order_by(ChatMemoryModel.timestamp.desc())
            .limit(count)
            .all()
        )

        models.reverse()  # 🔥 importante: orden cronológico

        return [self._model_to_entity(m) for m in models]

    # 🔁 Conversiones

    def _model_to_entity(self, model: ChatMemoryModel) -> ChatMessage:
        return ChatMessage(
            id=model.id,
            session_id=model.session_id,
            role=model.role,
            message=model.message,
            timestamp=model.timestamp,
        )

    def _entity_to_model(self, entity: ChatMessage) -> ChatMemoryModel:
        return ChatMemoryModel(
            session_id=entity.session_id,
            role=entity.role,
            message=entity.message,
            timestamp=entity.timestamp,
        )