from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    price: float
    quantity: int = 1

class CartItemCreate(BaseModel):
    product_id: int

class CartItemResponse(BaseModel):
    id: int
    product_id: int
    name: str
    price: float
    quantity: int

    class Config:
        orm_mode = True
