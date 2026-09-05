from sqlalchemy import (
    Column, Integer, String, Float, Date, ForeignKey, UniqueConstraint,
)
from sqlalchemy.orm import relationship
from backend.database import Base


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String)
    capacity = Column(Integer)

    inventory_items = relationship("Inventory", back_populates="store", cascade="all, delete-orphan")
    sales = relationship("DailySale", back_populates="store", cascade="all, delete-orphan")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String)
    unit_cost = Column(Float)
    retail_price = Column(Float)

    inventory_items = relationship("Inventory", back_populates="product", cascade="all, delete-orphan")
    sales = relationship("DailySale", back_populates="product", cascade="all, delete-orphan")
    lead_time = relationship("SupplierLeadTime", uselist=False, back_populates="product", cascade="all, delete-orphan")
    price_history = relationship("PriceHistory", back_populates="product", cascade="all, delete-orphan")


class DailySale(Base):
    __tablename__ = "daily_sales"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    revenue = Column(Float)

    store = relationship("Store", back_populates="sales")
    product = relationship("Product", back_populates="sales")

    __table_args__ = (
        UniqueConstraint("store_id", "product_id", "date", name="_store_product_date_uc"),
    )


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity_on_hand = Column(Integer, nullable=False, default=0)
    last_updated = Column(Date)

    store = relationship("Store", back_populates="inventory_items")
    product = relationship("Product", back_populates="inventory_items")

    __table_args__ = (
        UniqueConstraint("store_id", "product_id", name="_store_product_inv_uc"),
    )


class SupplierLeadTime(Base):
    __tablename__ = "supplier_lead_times"

    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    days = Column(Integer, nullable=False)

    product = relationship("Product", back_populates="lead_time")


class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    date = Column(Date, nullable=False)
    price = Column(Float, nullable=False)

    product = relationship("Product", back_populates="price_history")

    __table_args__ = (
        UniqueConstraint("product_id", "date", name="_product_date_price_uc"),
    )
