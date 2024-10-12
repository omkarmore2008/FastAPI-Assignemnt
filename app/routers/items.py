from fastapi import APIRouter, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from typing import List, Optional
from bson import ObjectId
from datetime import datetime, date
from app.config import client
from app.schemas import Item
from pydantic import EmailStr

from app.serializer import item_serializer, get_item_serializer
from app.config import get_collection

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)
@router.post("/", response_model=dict)
async def create_item(item: Item):
    item_dict = item_serializer(item.dict())
    item_dict["insert_date"] = str(datetime.now().date())
    items_collection = get_collection("items")
    result = items_collection.insert_one(item_dict)
    return {"msg": "Data inserted successfully"}

@router.get("/filter/items", response_model=List[dict])
async def get_items(
    email: Optional[EmailStr] = None,
    expiry_date: Optional[date] = None,
    insert_date: Optional[date] = None,
    quantity: Optional[int] = Query(None, ge=0)
):
    items = []
    query = {}
    if email:
        query["email"] = email
    if expiry_date:
        query["expiry_date"] = {"$gt": expiry_date}
    if insert_date:
        query["insert_date"] = {"$gt": insert_date}
    if quantity is not None:
        query["quantity"] = {"$gte": quantity}
    items_collection = get_collection("items")
    for item in items_collection.find(query):
        items.append(get_item_serializer(item))
    return items

@router.get("/{id}", response_model=dict)
async def get_item(id: str):
    items_collection = get_collection("items")
    item = items_collection.find_one({"_id": ObjectId(id)})
    if item:
        return get_item_serializer(item)
    raise HTTPException(status_code=404, detail="Item not found")

@router.put("/{id}", response_model=dict)
async def update_item(id: str, item: Item):
    item_dict = item_serializer(item.dict(exclude_unset=True))
    items_collection = get_collection("items")
    update_result = items_collection.update_one({"_id": ObjectId(id)}, {"$set": item_dict})

    if update_result.modified_count == 1:
        updated_item = items_collection.find_one({"_id": ObjectId(id)})
        if updated_item:
            return get_item_serializer(updated_item)
    raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/{id}")
async def delete_item(id: str):
    items_collection = get_collection("items")
    delete_result = items_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")
