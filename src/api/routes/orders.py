from fastapi import APIRouter, Depends, HTTPException

from src.services.order_service import OrderService
from src.api.schemas import OrderCreate, OrderResponse, OrderStatusUpdate
from src.dependencies import get_order_service

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/")
async def create_order(
    order_create: OrderCreate, order_service: OrderService = Depends(get_order_service)
):
    order = await order_service.create_order(order_create)
    return order


@router.get("/", response_model=list[OrderResponse])
async def get_orders(
    skip: int = 0,
    limit: int = 100,
    order_service: OrderService = Depends(get_order_service),
):
    return await order_service.get_orders(skip=skip, limit=limit)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int, order_service: OrderService = Depends(get_order_service)
):
    try:
        order = await order_service.get_order(order_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return order


@router.patch("/{order_id}/status")
async def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    order_service: OrderService = Depends(get_order_service),
):
    try:
        order = await order_service.update_status(order_id, status_update.status)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return order
