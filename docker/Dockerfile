# docker/Dockerfile
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Копировать requirements.txt
COPY requirements.txt .

# Установить зависимости
RUN pip install --no-cache-dir -r requirements.txt
COPY . .


# Открыть порт
EXPOSE 8000

# Запустить приложение
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]