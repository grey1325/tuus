import datetime
from enum import Enum
import html
import re
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_serializer,
    field_validator,
)
from decimal import Decimal


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200, description="Название товара")
    price: Decimal = Field(
        gt=0, le=10_000_000, description="Цена товара (должна быть больше 0)"
    )
    stock: int = Field(ge=0, le=100_000)
    category: str = Field(min_length=1, max_length=100)

    @field_validator("name")
    @classmethod
    def sanitize_name(cls, v: str) -> str:
        return html.escape(v.strip())

    @field_validator("category")
    @classmethod
    def sanitize_category(cls, value: str) -> str:
        if not re.match(r"^[A-Za-zА-Яа-я0-9\s-]+$", value):
            raise ValueError("Недопустимые символы в категории")
        return value


class ProductUpdate(BaseModel):
    """Модель для обновления товара"""

    name: str | None = Field(None, min_length=1, max_length=200)
    price: Decimal | None = Field(None, gt=0)
    stock: int | None = Field(None, ge=0)


class UserCreate(BaseModel):
    """Модель для создания пользователя"""

    name: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    """Модель для входа пользователя"""

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    """Модель для обновления пользователя"""

    name: str | None = Field(None, min_length=3, max_length=100)
    email: EmailStr | None = None


class OrderItemCreate(BaseModel):
    """Модель для создания товара в заказе"""

    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    """Модель для создания заказа"""

    user_id: int = Field(gt=0)
    items: list[OrderItemCreate]


class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class ProductResponse(BaseModel):
    id: int
    name: str
    price: Decimal
    stock: int

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("price")
    def serialize_price(self, value: Decimal) -> float:
        return float(value)


class ProductInOrderResponse(BaseModel):
    id: int
    name: str
    price: Decimal

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("price")
    def serialize_price(self, value: Decimal) -> float:
        return float(value)


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    balance: Decimal
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("balance")
    def serialize_balance(self, value: Decimal) -> float:
        return float(value)


class OrderItemResponse(BaseModel):
    product: ProductInOrderResponse
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total: Decimal
    status: OrderStatus
    order_date: datetime.datetime
    items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("total")
    def serialize_total(self, value: Decimal) -> float:
        return float(value)


class TokenResponse(BaseModel):
    """Ответ с JWT-токенами."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str
