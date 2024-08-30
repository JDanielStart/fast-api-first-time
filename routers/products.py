from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
        prefix="/products",
        tags=["products"],
        responses={404: {"message": "No encontrado"}},
    )

#Entidad product
product_list = [
            {"id": 1, "name": "Product 1", "price": 100},
            {"id": 2, "name": "Product 2", "price": 200},
            {"id": 3, "name": "Product 3", "price": 300}
        ]

@router.get("/")
async def read_products():
    return product_list

@router.get("/{id}")
async def read_product(id: int):
    return product_list[id-1]