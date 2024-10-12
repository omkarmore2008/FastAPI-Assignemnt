import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
APP_NAME = os.getenv("APP_NAME")

uri = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@cluster0.5acb8.mongodb.net/?retryWrites=true&w=majority&appName={APP_NAME}"
client = MongoClient(uri)

def get_collection(model):
    return client.assignemnt.get_collection(model)
