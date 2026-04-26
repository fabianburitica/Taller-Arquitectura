# 1. Imagen base ligera
FROM python:3.12-slim

# 2. Evitar archivos .pyc y buffer de logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Crear directorio de trabajo
WORKDIR /app

# 4. Copiar requirements primero (para cache)
COPY requirements.txt .

# 5. Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar todo el proyecto
COPY . .

# 7. Exponer puerto
EXPOSE 8000

# 8. Comando para correr la app
CMD ["uvicorn", "src.infrastructure.api.main:app", "--host", "0.0.0.0", "--port", "8000"]