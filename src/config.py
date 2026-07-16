from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL environment variable is not set")
ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
_secret_key = os.getenv("SECRET_KEY")
if _secret_key is None:
    raise RuntimeError("SECRET_KEY environment variable is not set")

SECRET_KEY: str = _secret_key

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))

REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))

_redis_url = os.getenv("REDIS_URL")
if _redis_url is None:
    raise RuntimeError("REDIS_URL environment variable is not set")
REDIS_URL: str = _redis_url
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
CACHE_TTL = 300

PRODUCTS_RATE_LIMIT = os.getenv("PRODUCTS_RATE_LIMIT", "30/minute")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
