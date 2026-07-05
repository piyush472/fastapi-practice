from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
app=FastAPI()

class Product(BaseModel):
    id:int
    name:str
    price:float

products=[
{"id": 1, "name": "Laptop", "price": 55000.0},
    {"id": 2, "name": "Mouse", "price": 500.0},
    {"id": 3, "name": "Keyboard", "price": 1200.0},

]


@app.get("/")
def home():
    return {"message": "hello"}


@app.get("/products",response_model=List[Product]) 
def get_products():
    return products

@app.get("/products/{id}")
def fetch_product(id: int):
    for p in products:
        if p["id"] == id:
            return p
    return {"error": "product not found"}

@app.post("/product")
def add_product(product:Product):
    products.append(product.model_dump())
    return product