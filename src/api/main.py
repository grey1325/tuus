import logging
import time


from fastapi.responses import JSONResponse

from slowapi import Limiter

from fastapi import FastAPI, Request, status


from src.exceptions.jwt_exceptions import ExpiredTokenError, InvalidTokenError
from src.exceptions.user_exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
)
from src.services.log_service import log_service


from slowapi.middleware import SlowAPIMiddleware
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from src.config import (
    CORS_ORIGINS,
)
from src.api.routes.products import router as products_router
from src.api.routes.users import router as users_router
from src.api.routes.orders import router as orders_router
from src.api.routes.auth import router as auth_router

app = FastAPI(title="TUUS API", version="1.0.0")


@app.exception_handler(UserAlreadyExistsError)
async def user_already_exists_handler(request: Request, exc: UserAlreadyExistsError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)}
    )


@app.exception_handler(InvalidCredentialsError)
async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(exc)}
    )


@app.exception_handler(InvalidTokenError)
async def invalid_token_handler(request: Request, exc: InvalidTokenError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(exc)}
    )


@app.exception_handler(ExpiredTokenError)
async def expired_token_handler(request: Request, exc: ExpiredTokenError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(exc)}
    )


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

app.include_router(products_router)
app.include_router(users_router)
app.include_router(orders_router)
app.include_router(auth_router)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
