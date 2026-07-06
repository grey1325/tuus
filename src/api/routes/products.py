from fastapi import APIRouter, Depends, HTTPException
from src.dependencies import get_product_service
from src.services import product_service
from src.api.schemas import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=list[ProductResponse])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    product_service: product_service.ProductService = Depends(get_product_service),
):
    return await product_service.get_products(skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    product_service: product_service.ProductService = Depends(get_product_service),
):
    try:
        product = await product_service.get_product(product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return product


@router.post("/")
async def create_product(
    product: ProductCreate,
    product_service: product_service.ProductService = Depends(get_product_service),
):
    return await product_service.create_product(product)


@router.put("/{product_id}")
async def update_product(
    product_id: int,
    product: ProductUpdate,
    product_service: product_service.ProductService = Depends(get_product_service),
):
    try:
        return await product_service.update_product(product_id, product)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    product_service: product_service.ProductService = Depends(get_product_service),
):
    try:
        await product_service.delete_product(product_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    return {"message": f"Товар {product_id} удалён"}
