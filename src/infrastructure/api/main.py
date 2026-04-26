from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

# DB
from src.infrastructure.db.database import get_db, init_db

# DTOs
from src.application.dtos import (
    ProductDTO,
    ChatMessageRequestDTO,
    ChatMessageResponseDTO,
    ChatHistoryDTO,
)

# Repositorios
from src.infrastructure.repositories.product_repository import SQLProductRepository
from src.infrastructure.repositories.chat_repository import SQLChatRepository

# Servicios
from src.application.product_service import ProductService
from src.application.chat_service import ChatService
from src.infrastructure.llm_providers.gemini_service import GeminiService

# Excepciones de dominio
from src.domain.exceptions import ProductNotFoundError


# 🚀 Crear app
app = FastAPI(
    title="E-Commerce Chat AI",
    description="API para e-commerce con chat inteligente usando Gemini",
    version="1.0.0",
)

# 🌐 CORS (permite frontend después)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ⚡ Evento startup
@app.on_event("startup")
def on_startup():
    init_db()


# =========================
# 📌 ENDPOINTS
# =========================

@app.get("/")
def root():
    return {
        "message": "E-Commerce Chat AI API",
        "version": "1.0.0",
        "endpoints": [
            "/products",
            "/products/{id}",
            "/chat",
            "/chat/history/{session_id}",
            "/health",
        ],
    }


# =========================
# 🛍 PRODUCTS
# =========================

@app.get("/products", response_model=List[ProductDTO])
def get_products(db: Session = Depends(get_db)):
    repo = SQLProductRepository(db)
    service = ProductService(repo)

    products = service.get_all_products()
    return [ProductDTO.from_orm(p) for p in products]


@app.get("/products/{product_id}", response_model=ProductDTO)
def get_product(product_id: int, db: Session = Depends(get_db)):
    repo = SQLProductRepository(db)
    service = ProductService(repo)

    try:
        product = service.get_product_by_id(product_id)
        return ProductDTO.from_orm(product)
    except ProductNotFoundError:
        raise HTTPException(status_code=404, detail="Producto no encontrado")


# =========================
# 💬 CHAT
# =========================

@app.post("/chat", response_model=ChatMessageResponseDTO)
async def chat(
    request: ChatMessageRequestDTO,
    db: Session = Depends(get_db),
):
    try:
        product_repo = SQLProductRepository(db)
        chat_repo = SQLChatRepository(db)
        ai_service = GeminiService()

        service = ChatService(product_repo, chat_repo, ai_service)

        response = await service.process_message(request)
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chat/history/{session_id}", response_model=List[ChatHistoryDTO])
def get_history(
    session_id: str,
    limit: Optional[int] = 10,
    db: Session = Depends(get_db),
):
    chat_repo = SQLChatRepository(db)
    product_repo = SQLProductRepository(db)
    ai_service = GeminiService()

    service = ChatService(product_repo, chat_repo, ai_service)

    return service.get_session_history(session_id, limit)


@app.delete("/chat/history/{session_id}")
def delete_history(session_id: str, db: Session = Depends(get_db)):
    chat_repo = SQLChatRepository(db)
    product_repo = SQLProductRepository(db)
    ai_service = GeminiService()

    service = ChatService(product_repo, chat_repo, ai_service)

    deleted = service.clear_session_history(session_id)

    return {"deleted_messages": deleted}


# =========================
# 🩺 HEALTH
# =========================

@app.get("/health")
def health():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow(),
    }