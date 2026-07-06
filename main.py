from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Product(BaseModel):
    id: int
    name: str
    price: float

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "hello"}

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@app.get("/products/{id}")
def fetch_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if product:
        return product
    return {"error": "product not found"}

@app.post("/product")
def add_product(product: Product, db: Session = Depends(get_db)):
    new_product = models.Product(
        id=product.id,
        name=product.name,
        price=product.price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.put("/product/{id}")
def update_products(id: int, product: Product, db: Session = Depends(get_db)):
    existing = db.query(models.Product).filter(models.Product.id == id).first()
    if not existing:
        return {"error": "product not found!"}
    existing.name = product.name
    existing.price = product.price
    db.commit()
    db.refresh(existing)
    return {"message": "product updated successfully!"}

@app.delete("/product/{id}")
def delete_products(id: int, db: Session = Depends(get_db)):
    existing = db.query(models.Product).filter(models.Product.id == id).first()
    if not existing:
        return {"error": "product not found!"}
    db.delete(existing)
    db.commit()
    return {"message": "product deleted successfully!"}