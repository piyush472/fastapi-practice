from decimal import Clamped

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    id:int
    name:str
    price:float
products = [
    {"id": 1, "name": "Laptop", "price": 55000.0},
    {"id": 2, "name": "Mouse", "price": 500.0},
    {"id": 3, "name": "Keyboard", "price": 1200.0},
]
app=FastAPI()

@app.get("/products",response_model=List[Product])
def get_all_products():
    return products