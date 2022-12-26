from pydantic import BaseModel


class TicketBase(BaseModel):
    title: str
    description: str | None = None

    class Config:
        orm_mode = True


class TicketCreate(TicketBase):
    pass


class Ticket(TicketBase):
    id: int
    ticket_owner_id: int

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: str
    model: str | None = None

    class Config:
        orm_mode = True


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    product_owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    tickets: list[Ticket] = []
    products: list[Product] = []

    class Config:
        orm_mode = True
