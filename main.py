
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
client = MongoClient("mongodb+srv://Aimaghribi:<your_password>@cluster0.hzbszls.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["aimaghribi"]
collection = db["clients"]

# FastAPI app
app = FastAPI()

# Allow frontend access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Client model
class Client(BaseModel):
    phone: str
    profession: str
    language: str

@app.post("/add-client")
def add_client(client: Client):
    if collection.find_one({"phone": client.phone}):
        raise HTTPException(status_code=400, detail="Client already exists")
    collection.insert_one({
        "phone": client.phone,
        "profession": client.profession,
        "language": client.language,
        "created_at": datetime.utcnow()
    })
    return {"message": "Client added successfully"}

@app.get("/clients")
def get_clients():
    clients = list(collection.find({}, {"_id": 0}))
    return clients

@app.delete("/client/{phone}")
def delete_client(phone: str):
    result = collection.delete_one({"phone": phone})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"message": "Client deleted successfully"}
