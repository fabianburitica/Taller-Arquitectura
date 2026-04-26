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


class ProductService:
    """
    Servicio de aplicación para gestionar productos.
    Orquesta la lógica entre DTOs, entidades y repositorio.
    """

    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository

    def get_all_products(self) -> List[Product]:
        return self.product_repository.get_all()

    def get_product_by_id(self, product_id: int) -> Product:
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(product_id)
        return product

    def search_products(self, filters: dict) -> List[Product]:
        products = self.product_repository.get_all()

        # Filtrado simple en memoria (luego puedes optimizar en DB)
        if "brand" in filters:
            products = [p for p in products if p.brand.lower() == filters["brand"].lower()]

        if "category" in filters:
            products = [p for p in products if p.category.lower() == filters["category"].lower()]

        if "min_price" in filters:
            products = [p for p in products if p.price >= filters["min_price"]]

        if "max_price" in filters:
            products = [p for p in products if p.price <= filters["max_price"]]

        return products

    def create_product(self, product_dto: ProductDTO) -> Product:
        try:
            product = Product(
                id=None,
                name=product_dto.name,
                brand=product_dto.brand,
                category=product_dto.category,
                size=product_dto.size,
                color=product_dto.color,
                price=product_dto.price,
                stock=product_dto.stock,
                description=product_dto.description
            )
        except ValueError as e:
            raise InvalidProductDataError(str(e))

        return self.product_repository.save(product)

    def update_product(self, product_id: int, product_dto: ProductDTO) -> Product:
        existing_product = self.product_repository.get_by_id(product_id)

        if not existing_product:
            raise ProductNotFoundError(product_id)

        try:
            updated_product = Product(
                id=product_id,
                name=product_dto.name,
                brand=product_dto.brand,
                category=product_dto.category,
                size=product_dto.size,
                color=product_dto.color,
                price=product_dto.price,
                stock=product_dto.stock,
                description=product_dto.description
            )
        except ValueError as e:
            raise InvalidProductDataError(str(e))

        return self.product_repository.save(updated_product)

    def delete_product(self, product_id: int) -> bool:
        existing_product = self.product_repository.get_by_id(product_id)

        if not existing_product:
            raise ProductNotFoundError(product_id)

        return self.product_repository.delete(product_id)

    def get_available_products(self) -> List[Product]:
        products = self.product_repository.get_all()
        return [p for p in products if p.is_available()]
        