from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, date
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class ItemBase(BaseModel):
    name: str = Field(..., example="Item A")
    email: EmailStr = Field(..., example="user@example.com")
    quantity: int = Field(..., ge=0, example=10)
    expiry_date: date = Field(..., example="2024-12-31")

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Updated Item")
    email: Optional[EmailStr] = Field(None, example="newuser@example.com")
    quantity: Optional[int] = Field(None, ge=0, example=20)
    expiry_date: Optional[date] = Field(None, example="2025-01-01")

class ItemInDB(ItemBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    insert_date: date = Field(default_factory=datetime.utcnow().date)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str, datetime: lambda dt: dt.isoformat()}

class ItemResponse(ItemBase):
    id: str
    insert_date: date

class ClockInBase(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    location: str = Field(..., example="New York")

class ClockInCreate(ClockInBase):
    pass

class ClockInUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, example="newuser@example.com")
    location: Optional[str] = Field(None, example="Los Angeles")

class ClockInInDB(ClockInBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    insert_date: date = Field(default_factory=datetime.utcnow().date)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str, datetime: lambda dt: dt.isoformat()}

class ClockInResponse(ClockInBase):
    id: str
    insert_date: date
