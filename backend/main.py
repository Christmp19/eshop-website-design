import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import Depends, FastAPI, HTTPException
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
    1: schemas.Product(id=1, name="Mens T-Shirt", price=19.99, img_url="/img/products/men/product1.jpg"),
    2: schemas.Product(id=2, name="Slim Khaki Trousers", price=34.99, img_url="/img/products/men/product2.jpg"),
    3: schemas.Product(id=3, name="Nike Shoes", price=89.99, img_url="/img/products/men/product3.jpg"),
    4: schemas.Product(id=4, name="Wrist Watch", price=59.99, img_url="/img/products/men/product4.jpg"),
    5: schemas.Product(id=5, name="V Neck Tassel Cape", price=24.99, img_url="/img/products/women/product1.jpg"),
    6: schemas.Product(id=6, name="Printed Wrap Dress", price=29.99, img_url="/img/products/women/product2.jpg"),
    7: schemas.Product(id=7, name="Blue Denim Dress", price=39.99, img_url="/img/products/women/product3.jpg"),
    8: schemas.Product(id=8, name="High Waist Denim Skirt", price=44.99, img_url="/img/products/women/product4.jpg"),
}

blog_posts_db = {
    1: schemas.BlogPost(id=1, title="Exciting New Features in Our Latest Update", excerpt="Discover the new features in our latest update that will enhance your experience and improve performance.", image_url="/img/posts/post1.jpg"),
    2: schemas.BlogPost(id=2, title="Tips and Tricks for a Better User Experience", excerpt="Explore some useful tips and tricks to make the most out of our platform and improve your user experience.", image_url="/img/posts/post2.jpg"),
    3: schemas.BlogPost(id=3, title="How to Optimize Your Website for Speed", excerpt="Learn how to optimize your website to improve loading times and provide a faster experience for your visitors.", image_url="/img/posts/post3.jpg"),
    4: schemas.BlogPost(id=4, title="Building a Successful E-commerce Strategy", excerpt="Delve into our comprehensive guide on building a successful e-commerce strategy that meets your business goals.", image_url="/img/posts/post4.jpg"),
    5: schemas.BlogPost(id=5, title="Understanding the Importance of Cybersecurity", excerpt="Cybersecurity is crucial in today's digital world. Learn why it's essential and how to protect your online presence.", image_url="/img/posts/post5.jpg"),
    6: schemas.BlogPost(id=6, title="Enhancing Web Accessibility for Better UX", excerpt="Explore methods to improve web accessibility, making your website usable for all, regardless of ability or disability.", image_url="/img/posts/post6.jpg"),
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
        db.commit()
        db.refresh(existing_cart_item)
        return existing_cart_item
    else:
        new_cart_item = models.CartItem(
            product_id=product.id,
            name=product.name,
            price=product.price,
            quantity=1,
            img_url=product.img_url
        )
        db.add(new_cart_item)
        db.commit()
        db.refresh(new_cart_item)
        return new_cart_item

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

@app.get("/blog/posts", response_model=List[schemas.BlogPost])
async def get_blog_posts():
    return list(blog_posts_db.values())

@app.get("/blog/posts/{post_id}", response_model=schemas.BlogPost)
async def get_blog_post(post_id: int):
    post = blog_posts_db.get(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return post