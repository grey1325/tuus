import json


import anthropic
from pydantic import BaseModel

from src.core.config import settings

async_client = anthropic.AsyncAnthropic(
    api_key=settings.anthropic_api_key,
)

CATEGORIES = [
    "Ноутбуки",
    "Смартфоны",
    "Планшеты",
    "Наушники",
    "Клавиатуры",
    "Мониторы",
    "Аксессуары",
]


class ProductCard(BaseModel):
    title: str
    description: str
    seo_keywords: list[str]
    category: str


async def generate_product_card(
    name: str,
    features: list[str],
    price: float,
) -> ProductCard:
    """SEO-описание + категория через structured output."""
    categories = ", ".join(CATEGORIES)
    response = await async_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        temperature=0.5,
        system=f"""Ты AI для генерации карточек товаров.
        Доступные категории:{categories}Верни ответ строго в JSON.""",
        messages=[
            {
                "role": "user",
                "content": f"Сгенерируй SEO-описание {name}"
                f"""с ключевыми словами: {features}.Цена: {price}. Верни в формате json: 
                {{"title": "...",
                "description": "...",
                "seo_keywords": [...],
                "category": "..."
                }}""",
            },
        ],
    )
    content = response.content[0].text
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("Claude вернул некорректный JSON")

    return ProductCard(**data)


async def categorize_batch(
    products: list[dict],
) -> list[str]:
    """Категоризация списка товаров через Haiku."""
    categories = ", ".join(CATEGORIES)
    products_json = json.dumps(products, ensure_ascii=False)
    response = await async_client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=500,
        temperature=0.1,
        system=f"""Ты AI для категоризации товаров.
        Доступные категории: {categories}. Верни ответ строго в JSON.""",
        messages=[
            {
                "role": "user",
                "content": f"Категоризуй список товаров: {products_json}",
            },
        ],
    )
    content = response.content[0].text
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("Claude вернул некорректный JSON")
    return data
