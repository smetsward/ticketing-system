from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    tickets = relationship("Ticket", back_populates="ticket_owner")
    products = relationship("Product", back_populates="product_owner")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    ticket_owner_id = Column(Integer, ForeignKey("users.id"))

    ticket_owner = relationship("User", back_populates="tickets")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    model = Column(String, index=True)
    product_owner_id = Column(Integer, ForeignKey("users.id"))

    product_owner = relationship("User", back_populates="products")
