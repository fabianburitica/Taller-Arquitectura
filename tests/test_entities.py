import pytest
from datetime import datetime

from src.domain.entities import Product, ChatMessage, ChatContext


# =========================
#  PRODUCT TESTS
# =========================

def test_product_valid_creation():
    product = Product(
        id=1,
        name="Nike Air",
        brand="Nike",
        category="Running",
        size="42",
        color="Negro",
        price=100.0,
        stock=10,
        description="Zapatillas cómodas"
    )
    assert product.name == "Nike Air"


def test_product_invalid_price():
    with pytest.raises(ValueError):
        Product(
            id=1,
            name="Nike Air",
            brand="Nike",
            category="Running",
            size="42",
            color="Negro",
            price=0,
            stock=10,
            description="Zapatillas"
        )


def test_product_negative_stock():
    with pytest.raises(ValueError):
        Product(
            id=1,
            name="Nike Air",
            brand="Nike",
            category="Running",
            size="42",
            color="Negro",
            price=100,
            stock=-1,
            description="Zapatillas"
        )


def test_is_available():
    product = Product(
        id=1,
        name="Nike Air",
        brand="Nike",
        category="Running",
        size="42",
        color="Negro",
        price=100,
        stock=5,
        description="Zapatillas"
    )
    assert product.is_available() is True


def test_reduce_stock():
    product = Product(
        id=1,
        name="Nike Air",
        brand="Nike",
        category="Running",
        size="42",
        color="Negro",
        price=100,
        stock=5,
        description="Zapatillas"
    )
    product.reduce_stock(2)
    assert product.stock == 3


def test_reduce_stock_error():
    product = Product(
        id=1,
        name="Nike Air",
        brand="Nike",
        category="Running",
        size="42",
        color="Negro",
        price=100,
        stock=1,
        description="Zapatillas"
    )
    with pytest.raises(ValueError):
        product.reduce_stock(5)


# =========================
#  CHAT MESSAGE TESTS
# =========================

def test_chat_message_valid():
    msg = ChatMessage(
        id=1,
        session_id="123",
        role="user",
        message="Hola",
        timestamp=datetime.utcnow()
    )
    assert msg.is_from_user() is True


def test_chat_message_invalid_role():
    with pytest.raises(ValueError):
        ChatMessage(
            id=1,
            session_id="123",
            role="admin",
            message="Hola",
            timestamp=datetime.utcnow()
        )


# =========================
#  CHAT CONTEXT TESTS
# =========================

def test_get_recent_messages():
    messages = [
        ChatMessage(None, "1", "user", f"msg{i}", datetime.utcnow())
        for i in range(10)
    ]
    context = ChatContext(messages=messages, max_messages=5)
    recent = context.get_recent_messages()

    assert len(recent) == 5


def test_format_for_prompt():
    messages = [
        ChatMessage(None, "1", "user", "Hola", datetime.utcnow()),
        ChatMessage(None, "1", "assistant", "Hola! ¿en qué puedo ayudarte?", datetime.utcnow())
    ]

    context = ChatContext(messages=messages)
    formatted = context.format_for_prompt()

    assert "Usuario: Hola" in formatted
    assert "Asistente:" in formatted