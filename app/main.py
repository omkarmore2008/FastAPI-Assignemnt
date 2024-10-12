from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routers import items, clock_in
app = FastAPI(
    title="FastAPI Assignemnt",
    version="0.1.0",
)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello Team!"}

app.include_router(items.router)
app.include_router(clock_in.router)
