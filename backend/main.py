import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import Depends, HTTPException
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from .database import SessionLocal, engine

app = FastAPI()

# Permettre l'accès CORS à votre API
origins = [
    "http://localhost",            # Frontend local
    "http://127.0.0.1:5501",       # Frontend local
    "http://localhost:8000",       # FastAPI local
    "https://eshop-website-design.vercel.app",  # URL Vercel ou autre
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connexion à la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Créez toutes les tables dans la base de données
models.Base.metadata.create_all(bind=engine)

# Simulation d'une base de données de produits
products_db = {
    1: schemas.Product(id=1, name="Mens T-Shirt", price=19.99),
    2: schemas.Product(id=2, name="Slim Khaki Trousers", price=34.99),
    3: schemas.Product(id=3, name="Nike Shoes", price=89.99),
    4: schemas.Product(id=4, name="Wrist Watch", price=59.99),
    5: schemas.Product(id=5, name="V Neck Tassel Cape", price=24.99),
    6: schemas.Product(id=6, name="Printed Wrap Dress", price=29.99),
    7: schemas.Product(id=7, name="Blue Denim Dress", price=39.99),
    8: schemas.Product(id=8, name="High Waist Denim Skirt", price=44.99),
}

@app.get("/")
async def root():
    return {"message": "Welcome to the Shopping API"}

@app.get("/products", response_model=List[schemas.Product])
async def get_products():
    return list(products_db.values())

@app.get("/cart", response_model=List[schemas.CartItemResponse])
async def get_cart(db: Session = Depends(get_db)):
    cart_items = db.query(models.CartItem).all()
    return cart_items

@app.post("/cart/add", response_model=schemas.CartItemResponse)
async def add_to_cart(cart_item: schemas.CartItemCreate, db: Session = Depends(get_db)):
    product_id = cart_item.product_id
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")

    product = products_db[product_id]
    existing_cart_item = db.query(models.CartItem).filter(models.CartItem.product_id == product_id).first()

    if existing_cart_item:
        existing_cart_item.quantity += 1
    else:
        new_cart_item = models.CartItem(
            product_id=product.id,
            name=product.name,
            price=product.price,
            quantity=1
        )
        db.add(new_cart_item)

    db.commit()
    db.refresh(existing_cart_item if existing_cart_item else new_cart_item)
    return existing_cart_item if existing_cart_item else new_cart_item

@app.delete("/cart/remove/{product_id}", response_model=schemas.CartItemResponse)
async def remove_from_cart(product_id: int, db: Session = Depends(get_db)):
    cart_item = db.query(models.CartItem).filter(models.CartItem.product_id == product_id).first()

    if cart_item:
        db.delete(cart_item)
        db.commit()
        return cart_item
    
    raise HTTPException(status_code=404, detail="Product not in cart")

@app.delete("/cart/clear")
async def clear_cart(db: Session = Depends(get_db)):
    db.query(models.CartItem).delete()
    db.commit()
    return {"message": "Cart cleared"}
