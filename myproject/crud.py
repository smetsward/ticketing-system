from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import auth
import models
import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_ticket(db: Session, id: int):
    return db.query(models.Ticket).filter(models.Ticket.id == id).first()


def get_products(db: Session, id: int):
    return db.query(models.Product).filter(models.Product.id == id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_ticket(db: Session, id: int, ticket: schemas.TicketBase):
    db_ticket = get_ticket(db=db, id=id)
    db_ticket.title = ticket.title
    db_ticket.description = ticket.description
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


def delete_ticket(db: Session, id: int):
    db_ticket = get_ticket(db=db, id=id)
    db.delete(db_ticket)
    db.commit()
    return db_ticket


def get_tickets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ticket).offset(skip).limit(limit).all()


def create_user_ticket(db: Session, ticket: schemas.TicketCreate, user_id: int):
    db_ticket = models.Ticket(**ticket.dict(), ticket_owner_id=user_id)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


def create_user_product(db: Session, product: schemas.ProductCreate, user_id: int):
    db_product = models.Product(**product.dict(), product_owner_id=user_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
