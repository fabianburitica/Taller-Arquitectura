from sqlalchemy.orm import Session
from src.infrastructure.db.models import ProductModel


def load_initial_data(db: Session):
    # Verificar si ya hay productos
    if db.query(ProductModel).count() > 0:
        print("✔ Datos ya cargados")
        return

    products = [
        ProductModel(
            name="Nike Air Max",
            brand="Nike",
            category="Running",
            size="42",
            color="Negro",
            price=120,
            stock=10,
            description="Zapatillas cómodas para correr"
        ),
        ProductModel(
            name="Adidas Ultraboost",
            brand="Adidas",
            category="Running",
            size="41",
            color="Blanco",
            price=150,
            stock=8,
            description="Alto rendimiento y comodidad"
        ),
        ProductModel(
            name="Puma RS-X",
            brand="Puma",
            category="Casual",
            size="43",
            color="Rojo",
            price=90,
            stock=15,
            description="Estilo urbano moderno"
        ),
        ProductModel(
            name="Nike Court Vision",
            brand="Nike",
            category="Casual",
            size="40",
            color="Blanco",
            price=85,
            stock=20,
            description="Diseño clásico y elegante"
        ),
        ProductModel(
            name="Adidas Stan Smith",
            brand="Adidas",
            category="Casual",
            size="42",
            color="Verde",
            price=95,
            stock=12,
            description="Icono del estilo casual"
        ),
        ProductModel(
            name="Puma Future Rider",
            brand="Puma",
            category="Running",
            size="41",
            color="Azul",
            price=80,
            stock=10,
            description="Ligereza y comodidad"
        ),
        ProductModel(
            name="Nike Air Force 1",
            brand="Nike",
            category="Casual",
            size="43",
            color="Blanco",
            price=110,
            stock=18,
            description="Clásico urbano"
        ),
        ProductModel(
            name="Adidas Samba",
            brand="Adidas",
            category="Formal",
            size="42",
            color="Negro",
            price=100,
            stock=6,
            description="Elegancia deportiva"
        ),
        ProductModel(
            name="Puma Smash",
            brand="Puma",
            category="Casual",
            size="40",
            color="Negro",
            price=70,
            stock=14,
            description="Minimalista y cómodo"
        ),
        ProductModel(
            name="Nike Pegasus",
            brand="Nike",
            category="Running",
            size="41",
            color="Gris",
            price=130,
            stock=9,
            description="Excelente amortiguación"
        ),
    ]

    db.add_all(products)
    db.commit()

    print("🔥 Datos iniciales cargados correctamente")