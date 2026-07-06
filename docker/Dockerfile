# docker/Dockerfile
FROM python:3.11-slim as builder

WORKDIR /app

# Копировать requirements.txt
COPY requirements.txt .

# Установить зависимости
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

FROM python:3.11-slim
# Копировать код приложения
WORKDIR /app

COPY --from=builder /app /app
# Открыть порт
EXPOSE 8000

# Запустить приложение
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]