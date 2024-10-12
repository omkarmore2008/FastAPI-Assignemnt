from pydantic import BaseModel, EmailStr
from datetime import date


class Item(BaseModel):
    name: str
    email: EmailStr
    item_name: str
    quantity: int
    expiry_date: date
