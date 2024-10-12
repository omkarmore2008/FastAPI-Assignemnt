# app/routers/clock_in.py

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from pydantic import EmailStr  # Add this import

from app.models import (
    ClockInCreate,
    ClockInUpdate,
    ClockInResponse,
)
from app.config import get_collection

router = APIRouter(
    prefix="/clock-in",
    tags=["Clock-In Records"]
)

clock_in_collection = get_collection("clock_in_records")

@router.post("/", response_model=ClockInResponse, status_code=201)
async def create_clock_in(record: ClockInCreate):
    record_dict = record.dict()
    record_dict["insert_date"] = str(datetime.now().date())
    result = clock_in_collection.insert_one(record_dict)
    new_record = clock_in_collection.find_one({"_id": result.inserted_id})
    return ClockInResponse(
        id=str(new_record["_id"]),
        email=new_record["email"],
        location=new_record["location"],
        insert_date=new_record["insert_date"]
    )

@router.get("/{id}", response_model=ClockInResponse)
async def get_clock_in(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    record = clock_in_collection.find_one({"_id": ObjectId(id)})
    if record is None:
        raise HTTPException(status_code=404, detail="Clock-In record not found")
    return ClockInResponse(
        id=str(record["_id"]),
        email=record["email"],
        location=record["location"],
        insert_date=record["insert_date"]
    )

@router.get("/filter/clock-in", response_model=List[ClockInResponse])
async def filter_clock_ins(
    email: Optional[EmailStr] = Query(None, description="Filter by exact email"),
    location: Optional[str] = Query(None, description="Filter by exact location"),
    insert_date: Optional[datetime] = Query(None, description="Clock-ins after this datetime")
):
    query = {}
    if email:
        query["email"] = email
    if location:
        query["location"] = location
    if insert_date:
        query["insert_date"] = {"$gt": insert_date}
    
    cursor = clock_in_collection.find(query)
    results = []
    for record in cursor:
        results.append(ClockInResponse(
            id=str(record["_id"]),
            email=record["email"],
            location=record["location"],
            insert_date=record["insert_date"]
        ))
    return results

@router.delete("/{id}", status_code=204)
async def delete_clock_in(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    result = clock_in_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Clock-In record not found")
    return

@router.put("/{id}", response_model=ClockInResponse)
async def update_clock_in(id: str, record: ClockInUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    update_data = {k: v for k, v in record.dict().items() if v is not None}
    if update_data:
        result = clock_in_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Clock-In record not found")
    record_updated = clock_in_collection.find_one({"_id": ObjectId(id)})
    return ClockInResponse(
        id=str(record_updated["_id"]),
        email=record_updated["email"],
        location=record_updated["location"],
        insert_date=record_updated["insert_date"]
    )
