from dotenv import load_dotenv
import os
import google.generativeai as genai

from src.domain.entities import Product, ChatContext
from src.domain.exceptions import ChatServiceError

# Cargar variables de entorno (.env)
load_dotenv()


class GeminiService:
    """
    Servicio para interactuar con Google Gemini
    """

    def __init__(self):
        # 🔑 Obtener API KEY
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY no está configurada")

        # 🔧 Configurar cliente
        genai.configure(api_key=api_key)

        # 🤖 Modelo
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    async def generate_response(
        self,
        user_message: str,
        products: list[Product],
        context: ChatContext
    ) -> str:
        """
        Genera respuesta usando Gemini
        """
        try:
            # 1. Formatear productos
            products_text = self.format_products_info(products)

            # 2. Formatear contexto
            context_text = context.format_for_prompt()

            # 3. Construir prompt
            prompt = f"""
Eres un asistente virtual experto en ventas de zapatos para un e-commerce.
Tu objetivo es ayudar a los clientes a encontrar los zapatos perfectos.

PRODUCTOS DISPONIBLES:
{products_text}

INSTRUCCIONES:
- Sé amigable y profesional
- Usa el contexto de la conversación anterior
- Recomienda productos específicos cuando sea apropiado
- Menciona precios, tallas y disponibilidad
- Si no tienes información, sé honesto

{context_text}

Usuario: {user_message}

Asistente:
"""

            # 4. Llamar a Gemini
            response = self.model.generate_content(prompt)

            # 5. Retornar respuesta
            return response.text.strip()

        except Exception as e:
            raise ChatServiceError(f"Error con Gemini: {str(e)}")

    def format_products_info(self, products: list[Product]) -> str:
        """
        Convierte productos a texto legible para el prompt
        """
        if not products:
            return "No hay productos disponibles."

        lines = []
        for p in products:
            lines.append(
                f"- {p.name} | {p.brand} | ${p.price} | Stock: {p.stock} | Talla: {p.size}"
            )

        return "\n".join(lines)