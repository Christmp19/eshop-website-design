from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    price: float
    img_url: str

    class Config:
        from_attributes = True

class CartItemCreate(BaseModel):
    product_id: int

class CartItemResponse(BaseModel):
    id: int
    product_id: int
    name: str
    price: float
    quantity: int
    img_url: str

    class Config:
        from_attributes = True

# Nouveau schéma pour les articles de blog
class BlogPost(BaseModel):
    id: int
    title: str
    excerpt: str
    image_url: str

    class Config:
        from_attributes = True
