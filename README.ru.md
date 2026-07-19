# TUUS — Modern FastAPI E-commerce Backend

<div align="center">

**Production-inspired backend интернет-магазина, разработанный на FastAPI**

*Асинхронная архитектура • PostgreSQL • Redis • JWT • Docker • SQLAlchemy 2.0 • Pytest*


</div>

---

# О проекте

**TUUS** — backend интернет-магазина, разработанный с использованием современных технологий Python.

Проект начинался как учебный, однако постепенно был переработан и приближен к архитектуре коммерческих backend-приложений.

Главной целью было не просто реализовать CRUD-операции, а построить масштабируемую архитектуру с разделением ответственности, асинхронной обработкой запросов, кэшированием, системой аутентификации и полноценным тестированием.

---

# Основные возможности

## Пользователи

* регистрация
* авторизация
* получение текущего пользователя
* обновление профиля
* удаление пользователя

---

## JWT Authentication

* Access Token
* Refresh Token
* обновление токенов
* защищённые эндпоинты

---

## Каталог товаров

* создание товара
* просмотр каталога
* просмотр отдельного товара
* обновление товара
* удаление товара
* поиск товаров

---

## Заказы

* создание заказа
* изменение статуса
* просмотр заказов
* автоматический расчёт стоимости
* проверка остатков товаров

---

## Производительность

* Redis Cache
* автоматическая инвалидация кэша
* асинхронная работа с PostgreSQL

---

## Тестирование

* Unit Tests
* API Tests
* Integration Tests

---

# Используемые технологии

| Категория        | Технологии                    |
| ---------------- | ----------------------------- |
| Backend          | Python 3.13, FastAPI          |
| ORM              | SQLAlchemy 2.0 Async          |
| Database         | PostgreSQL                    |
| Cache            | Redis                         |
| Authentication   | JWT                           |
| Password Hashing | bcrypt / Passlib              |
| Validation       | Pydantic v2                   |
| Testing          | pytest, pytest-asyncio, httpx |
| Infrastructure   | Docker, Docker Compose        |
| Migrations       | Alembic                       |

---

# Архитектура

Проект построен по многослойной архитектуре.

```text
                    HTTP Request
                         │
                         ▼
                  FastAPI Router
                         │
                         ▼
                Dependency Injection
                         │
                         ▼
                    Service Layer
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
 Repository Layer                 Cache Layer
          │                             │
          ▼                             ▼
 PostgreSQL                       Redis Cache
```

## Основные принципы

* Repository Pattern
* Service Layer
* Dependency Injection
* DTO через Pydantic
* Единая транзакция на запрос
* Централизованная обработка исключений
* Асинхронная работа с БД
* Инвалидация кэша после изменения данных

---

# Структура проекта

```text
src/
│
├── api/
│   ├── routes/
│   ├── schemas.py
│   └── main.py
│
├── database/
│   ├── connection.py
│   └── models.py
│
├── repositories/
│
├── services/
│
├── exceptions/
│
├── dependencies.py
│
└── tests/
    ├── api/
    ├── integration/
    ├── services/
    └── conftest.py
```

---

# Запуск проекта

## Через Docker

```bash
docker compose up --build
```

---

## Локально

```bash
git clone <repository>

cd TUUS

python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt

alembic upgrade head

uvicorn src.api.main:app --reload
```

---

# Запуск тестов

Все тесты

```bash
pytest
```

Unit

```bash
pytest src/tests/services
```

API

```bash
pytest src/tests/api
```

Integration

```bash
pytest src/tests/integration
```

---

# Документация API

После запуска приложения:

```
/docs
```

Swagger UI

```
/redoc
```

ReDoc

---

# Что демонстрирует этот проект

Проект создавался не только для реализации функциональности интернет-магазина, но и для демонстрации практических навыков backend-разработки.

В частности, в проекте реализованы:

* построение многослойной архитектуры;
* разделение бизнес-логики и слоя доступа к данным;
* работа с асинхронным SQLAlchemy;
* Dependency Injection;
* JWT-аутентификация;
* Redis-кэширование;
* централизованная обработка ошибок;
* Docker-инфраструктура;
* покрытие проекта несколькими уровнями тестирования.

---

# Возможные направления развития

* роли пользователей;
* корзина;
* категории товаров;
* изображения товаров;
* оформление оплаты;
* история заказов;
* email-уведомления;
* мониторинг (Prometheus + Grafana);
* CI/CD с автоматическим деплоем;
* Kubernetes.

---

# Автор

Проект разработан как часть профессиональной подготовки Backend Python Developer.

Основной акцент сделан на архитектуру, качество кода, тестируемость и использование современных практик разработки.
