import logging
import time


from slowapi import Limiter

from fastapi import (
    APIRouter,
    FastAPI,
    Request,
)


from src.services.log_service import log_service


from slowapi.middleware import SlowAPIMiddleware
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from passlib.context import CryptContext
from src.config import (
    CORS_ORIGINS,
)
from src.api.routes.products import router as products_router
from src.api.routes.users import router as users_router
from src.api.routes.orders import router as orders_router

app = FastAPI(title="SFMShop API", version="1.0.0")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    log_service.info(f"Получен запрос: {request.method} {request.url.path}")
    response = await call_next(request)
    process_time = time.time() - start_time
    log_service.info(
        f"Ответ: {response.status_code}, " f"время выполнения: {process_time:.4f} сек"
    )
    return response


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)
limiter = Limiter(key_func=get_remote_address)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
app.add_middleware(SlowAPIMiddleware)
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)


v1_router = APIRouter(prefix="/api/v1", tags=["v1"])


@v1_router.get("/products")
async def get_products_v1():
    return {"products": [{"id": 1, "name": "Ноутбук", "price": 50000}]}


# Версия 2
v2_router = APIRouter(prefix="/api/v2", tags=["v2"])


@v2_router.get("/products")
async def get_products_v2():
    return {
        "products": [{"id": 1, "name": "Ноутбук", "price": 50000}],
        "metadata": {"total": 1, "page": 1, "per_page": 10},
    }


app.include_router(v1_router)
app.include_router(v2_router)
app.include_router(products_router)
app.include_router(users_router)
app.include_router(orders_router)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
