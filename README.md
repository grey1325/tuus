# TUUS — Modern FastAPI E-Commerce Backend

<div align="center">

**A production-inspired e-commerce backend built with FastAPI**

*Asynchronous Architecture • PostgreSQL • Redis • JWT • Docker • SQLAlchemy 2.0 • Pytest*


</div>

---

# About the Project

**TUUS** is a modern e-commerce backend built with **FastAPI** and designed using production-oriented architectural principles.

Originally started as a learning project, it gradually evolved into a portfolio application focused on clean architecture, asynchronous programming, scalability, and maintainability.

The primary goal was not only to implement standard CRUD operations, but also to demonstrate practical backend development skills commonly used in commercial Python projects.

---

# Features

## User Management

* User registration
* User authentication
* Current user endpoint
* Update user profile
* Delete users

---

## JWT Authentication

* Access Tokens
* Refresh Tokens
* Token refresh endpoint
* Protected API endpoints

---

## Product Catalog

* Create products
* Retrieve product list
* Retrieve product details
* Update products
* Delete products
* Product search

---

## Order Management

* Create orders
* Update order status
* Retrieve orders
* Automatic order total calculation
* Stock availability validation

---

## Performance

* Redis caching
* Automatic cache invalidation
* Asynchronous PostgreSQL access

---

## Testing

* Unit Tests
* API Tests
* Integration Tests

---

# Technology Stack

| Category            | Technologies                  |
| ------------------- | ----------------------------- |
| Language            | Python 3.13                   |
| Framework           | FastAPI                       |
| ORM                 | SQLAlchemy 2.0 (Async)        |
| Database            | PostgreSQL                    |
| Cache               | Redis                         |
| Authentication      | JWT                           |
| Password Hashing    | Passlib + bcrypt              |
| Validation          | Pydantic v2                   |
| Testing             | Pytest, Pytest-Asyncio, HTTPX |
| Infrastructure      | Docker, Docker Compose        |
| Database Migrations | Alembic                       |

---

# Architecture

The project follows a layered architecture with clear separation of responsibilities.

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

## Architectural Principles

* Repository Pattern
* Service Layer
* Dependency Injection
* Data Transfer Objects (Pydantic)
* One transaction per request
* Centralized exception handling
* Asynchronous database access
* Automatic cache invalidation

---

# Project Structure

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

# Getting Started

## Run with Docker

```bash
docker compose up --build
```

---

## Local Development

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

# Running Tests

Run all tests

```bash
pytest
```

Run unit tests

```bash
pytest src/tests/services
```

Run API tests

```bash
pytest src/tests/api
```

Run integration tests

```bash
pytest src/tests/integration
```

---

# API Documentation

After starting the application:

```
/docs
```

Swagger UI

```
/redoc
```

ReDoc

---

# What This Project Demonstrates

This project was created not only to build an online store backend but also to showcase practical backend development skills.

Key concepts demonstrated include:

* Layered architecture
* Separation of business logic and data access
* Asynchronous SQLAlchemy
* Dependency Injection
* JWT Authentication
* Redis caching
* Centralized exception handling
* Dockerized deployment
* Multi-level testing strategy

---

# Future Improvements

* Role-based authorization
* Shopping cart
* Product categories
* Product image uploads
* Payment integration
* Order history
* Email notifications
* Monitoring with Prometheus & Grafana
* CI/CD pipeline
* Kubernetes deployment

---

# Author

This project was developed as part of my professional Backend Python Developer journey.

Its primary focus is on clean architecture, code quality, maintainability, testing, and modern backend development practices.