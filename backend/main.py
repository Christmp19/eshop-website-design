import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Dict, List
import models
import schemas
from .database import SessionLocal, engine

app = FastAPI()

# Permettre l'accès CORS à votre API
origins = [
    "http://localhost",            # Frontend local
    "http://localhost:3000"         # Frontend
    "http://127.0.0.1:5501",       # Frontend local
    "http://localhost:8000",       # FastAPI local
    "https://eshop-website-design.vercel.app",  # URL Vercel ou autre
     "*"                             # Pour permettre toutes les origines
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
    # Produits pour Hommes
    1: schemas.Product(id=1, name="Mens T-Shirt", price=19.99, img_url="/img/products/men/product1.jpg"),
    2: schemas.Product(id=2, name="Slim Khaki Trousers", price=34.99, img_url="/img/products/men/product2.jpg"),
    3: schemas.Product(id=3, name="Nike Shoes", price=89.99, img_url="/img/products/men/product3.jpg"),
    4: schemas.Product(id=4, name="Wrist Watch", price=59.99, img_url="/img/products/men/product4.jpg"),
    5: schemas.Product(id=5, name="Leather Jacket", price=99.99, img_url="/img/products/men/product5.jpg"),
    6: schemas.Product(id=6, name="Formal Shirt", price=45.00, img_url="/img/products/men/product6.jpg"),
    7: schemas.Product(id=7, name="Sports Shorts", price=25.00, img_url="/img/products/men/product7.jpg"),
    8: schemas.Product(id=8, name="Casual Hoodie", price=55.00, img_url="/img/products/men/product8.jpg"),
    9: schemas.Product(id=9, name="Running Shoes", price=75.99, img_url="/img/products/men/product9.jpg"),
    10: schemas.Product(id=10, name="Denim Jeans", price=59.50, img_url="/img/products/men/product10.jpg"),

    # Produits pour Femmes
    11: schemas.Product(id=11, name="V Neck Tassel Cape", price=24.99, img_url="/img/products/women/product1.jpg"),
    12: schemas.Product(id=12, name="Printed Wrap Dress", price=29.99, img_url="/img/products/women/product2.jpg"),
    13: schemas.Product(id=13, name="Blue Denim Dress", price=39.99, img_url="/img/products/women/product3.jpg"),
    14: schemas.Product(id=14, name="High Waist Denim Skirt", price=44.99, img_url="/img/products/women/product4.jpg"),
    15: schemas.Product(id=15, name="Chiffon Blouse", price=19.99, img_url="/img/products/women/product5.jpg"),
    16: schemas.Product(id=16, name="Stiletto Heels", price=49.99, img_url="/img/products/women/product6.jpg"),
    17: schemas.Product(id=17, name="Leather Handbag", price=69.99, img_url="/img/products/women/product7.jpg"),
    18: schemas.Product(id=18, name="Sports Leggings", price=29.50, img_url="/img/products/women/product8.jpg"),
    19: schemas.Product(id=19, name="Cashmere Scarf", price=35.00, img_url="/img/products/women/product9.jpg"),
    20: schemas.Product(id=20, name="Evening Gown", price=119.99, img_url="/img/products/women/product10.jpg"),

    # Produits pour Enfants
    21: schemas.Product(id=21, name="Kids T-Shirt", price=12.99, img_url="/img/products/kids/product1.jpg"),
    22: schemas.Product(id=22, name="Cartoon Hoodie", price=18.99, img_url="/img/products/kids/product2.jpg"),
    23: schemas.Product(id=23, name="Denim Shorts", price=14.99, img_url="/img/products/kids/product3.jpg"),
    24: schemas.Product(id=24, name="Sneakers", price=29.99, img_url="/img/products/kids/product4.jpg"),
    25: schemas.Product(id=25, name="Summer Hat", price=9.99, img_url="/img/products/kids/product5.jpg"),
    26: schemas.Product(id=26, name="School Backpack", price=24.99, img_url="/img/products/kids/product6.jpg"),
    27: schemas.Product(id=27, name="Rain Boots", price=19.99, img_url="/img/products/kids/product7.jpg"),
    28: schemas.Product(id=28, name="Boys Jacket", price=34.99, img_url="/img/products/kids/product8.jpg"),
    29: schemas.Product(id=29, name="Girls Dress", price=22.99, img_url="/img/products/kids/product9.jpg"),
    30: schemas.Product(id=30, name="Play Sandals", price=15.99, img_url="/img/products/kids/product10.jpg"),
}

@app.get("/products/home", response_model=Dict[str, List[schemas.Product]])
async def get_home_products():
    # Séparer les produits en trois catégories
    mens_products = [product for product in products_db.values() if 1 <= product.id <= 10][:4]
    womens_products = [product for product in products_db.values() if 11 <= product.id <= 20][:4]
    kids_products = [product for product in products_db.values() if 21 <= product.id <= 30][:4]

    # Retourner les produits limités pour la page d'accueil
    return {
        "men": mens_products,
        "women": womens_products,
        "kids": kids_products
    }

@app.get("/products", response_model=Dict[str, List[schemas.Product]])
async def get_products():
    # Séparer les produits en trois catégories
    mens_products = [product for product in products_db.values() if 1 <= product.id <= 10]
    womens_products = [product for product in products_db.values() if 11 <= product.id <= 20]
    kids_products = [product for product in products_db.values() if 21 <= product.id <= 30]

    # Retourner tous les produits
    return {
        "men": mens_products,
        "women": womens_products,
        "kids": kids_products
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
