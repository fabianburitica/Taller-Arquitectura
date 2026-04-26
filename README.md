# E-Commerce Chat AI

## Descripción del Proyecto

Este proyecto implementa una API REST usando FastAPI que integra un
chatbot con inteligencia artificial (Google Gemini) para ayudar a los
usuarios a encontrar productos en un catálogo de zapatos.

El sistema utiliza una arquitectura limpia (Clean Architecture),
separando dominio, aplicación e infraestructura.

------------------------------------------------------------------------

## Características Principales

-   Chat inteligente con Google Gemini
-   Memoria conversacional por sesión
-   Gestión de productos
-   API REST con FastAPI
-   Base de datos SQLite
-   Testing con Pytest
-   Containerización con Docker

------------------------------------------------------------------------

## Arquitectura

Estructura:

src/
 ├── domain/           # Lógica de negocio
 ├── application/      # Casos de uso
 └── infrastructure/   # API, base de datos, IA

Flujo: Usuario → API → ChatService → Gemini → Respuesta

------------------------------------------------------------------------

## Instalación

1.  Clonar repositorio

git clone https://github.com/fabianburitica/Taller-Arquitectura.git

cd e-commerce-chat-ai

2.  Crear entorno virtual

python -m venv venv

venv\Scripts\activate

3.  Instalar dependencias

pip install -r requirements.txt

------------------------------------------------------------------------

## Configuración

Crear archivo .env:

GEMINI_API_KEY=tu_api_key
DATABASE_URL=sqlite:///./data/ecommerce_chat.db
ENVIRONMENT=development

------------------------------------------------------------------------

## Uso

Ejecutar la API:

uvicorn src.infrastructure.api.main:app --reload

Abrir en navegador:

http://127.0.0.1:8000/docs

------------------------------------------------------------------------

## Ejemplo de uso

POST /chat

{
  "session_id": "user1",
  "message": "Busco zapatillas Nike"
}

Respuesta:

{ "session_id": "user1", "user_message": "Busco zapatillas Nike",
"assistant_message": "Te recomiendo...", "timestamp": "2026-..." }

------------------------------------------------------------------------

## Testing

Ejecutar:

pytest

Resultado esperado:

11 passed

------------------------------------------------------------------------

## Docker

Construir imagen:

docker build -t ecommerce-api .

Ejecutar contenedor:

docker run -p 8000:8000 --env-file .env ecommerce-api

Con docker-compose:

docker compose up --build

------------------------------------------------------------------------

## Tecnologías Utilizadas

-   Python 3.12
-   FastAPI
-   SQLAlchemy
-   SQLite
-   Pydantic
-   Google Gemini AI
-   Pytest
-   Docker

------------------------------------------------------------------------

## Estructura del Proyecto

e-commerce-chat-ai/
 ├── src/
 ├── tests/
 ├── data/
 ├── evidencias/
 ├── Dockerfile
 ├── docker-compose.yml
 ├── requirements.txt
 ├── pyproject.toml
 └── README.md

------------------------------------------------------------------------

## Autor

Fabián Buriticá

------------------------------------------------------------------------

## Notas

-   El sistema utiliza inteligencia artificial para generar
    recomendaciones
-   Mantiene contexto conversacional por sesión
-   Proyecto con fines educativos
