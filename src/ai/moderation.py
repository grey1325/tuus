import json
from typing import Literal

import anthropic
from pydantic import BaseModel

from src.core.config import settings

async_client = anthropic.AsyncAnthropic(
    api_key=settings.anthropic_api_key,
)


class ModerationResult(BaseModel):
    is_approved: bool
    sentiment: Literal["positive", "neutral", "negative"]
    is_spam: bool
    has_profanity: bool
    rejection_reason: str | None = None
    clean_text: str | None = None


async def moderate_review(
    text: str,
) -> ModerationResult:
    """Модерация отзыва."""
    response = await async_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        temperature=0,
        system="Ты модератор, проверяющий отзывы. Верни ответ строго в JSON.",
        messages=[
            {
                "role": "user",
                "content": f"""Модерируй отзыв: {text}. 
                Верни в формате json: 
                {{"is_approved": ...,
                "sentiment": ...,
                "is_spam": ...,
                "has_profanity": ...,
                "rejection_reason": ...,
                "clean_text": ...}}""",
            },
        ],
    )
    content = response.content[0].text
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("Claude вернул некорректный JSON")
    data["is_approved"] = not data["is_spam"] and not data["has_profanity"]
    data.setdefault("rejection_reason", None)
    data.setdefault("clean_text", None)

    return ModerationResult(**data)
