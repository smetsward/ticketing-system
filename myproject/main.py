import os

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import auth
import crud
import models
import schemas
from database import SessionLocal, engine

print("We are in the main.......")
if not os.path.exists('.\sqlitedb'):
    print("Making folder.......")
    os.makedirs('.\sqlitedb')

print("Creating tables.......")
models.Base.metadata.create_all(bind=engine)
print("Tables created.......")

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/token", tags=["Authorize"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", tags=["Users"], response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", tags=["Users"], response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/me", tags=["Users"], response_model=schemas.User)
def read_users_me(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = auth.get_current_active_user(db, token)
    return current_user


@app.get("/users/{user_id}", tags=["Users"], response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/tickets/", tags=["Tickets"], response_model=schemas.Ticket)
def create_ticket_for_user(
        user_id: int, ticket: schemas.TicketCreate, db: Session = Depends(get_db)
):
    return crud.create_user_ticket(db=db, ticket=ticket, user_id=user_id)


@app.post("/users/{user_id}/products/", tags=["Products"], response_model=schemas.Product)
def create_product_for_user(
        user_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)
):
    return crud.create_user_product(db=db, product=product, user_id=user_id)


@app.get("/tickets/", tags=["Tickets"], response_model=list[schemas.Ticket])
def read_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    tickets = crud.get_tickets(db, skip=skip, limit=limit)
    return tickets


@app.get("/tickets/{id}", tags=["Tickets"], response_model=schemas.Ticket)
def read_ticket(id: int, db: Session = Depends(get_db)):
    db_ticket = crud.get_ticket(db, id=id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_ticket


@app.put("/tickets/{id}", tags=["Tickets"], response_model=schemas.TicketBase)
async def update_ticket(id: int, ticket: schemas.TicketBase, db: Session = Depends(get_db)):
    return crud.update_ticket(db, id=id, ticket=ticket)


@app.delete("/tickets/{id}", tags=["Tickets"])
async def delete_ticket(id: int, db: Session = Depends(get_db)):
    return crud.delete_ticket(db, id=id)
