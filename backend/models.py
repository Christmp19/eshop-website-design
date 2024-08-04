from sqlalchemy import Column, Integer, String, Float
from backend.database import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    quantity = Column(Integer, default=1)
