from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
from auth import hash_password, verify_password, create_access_token, decode_access_token

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class Product(BaseModel):
    id: int
    name: str
    price: float

class UserCreate(BaseModel):
    username: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# checks the token sent with a request and returns the logged-in username
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="invalid token")
        return username
    except:
        raise HTTPException(status_code=401, detail="invalid or expired token")

@app.get("/")
def home():
    return {"message": "hello"}

# creates a new user with a hashed (not plain text) password
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="username already taken")
    new_user = models.User(username=user.username, hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    return {"message": "user created successfully"}

# checks credentials, returns a JWT token if correct
@app.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="invalid credentials")
    token = create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}

# protected: requires a valid token to access
@app.get("/products")
def get_products(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return db.query(models.Product).all()

@app.get("/products/{id}")
def fetch_product(id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if product:
        return product
    return {"error": "product not found"}

@app.post("/product")
def add_product(product: Product, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    new_product = models.Product(id=product.id, name=product.name, price=product.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.put("/product/{id}")
def update_products(id: int, product: Product, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    existing = db.query(models.Product).filter(models.Product.id == id).first()
    if not existing:
        return {"error": "product not found!"}
    existing.name = product.name
    existing.price = product.price
    db.commit()
    db.refresh(existing)
    return {"message": "product updated successfully!"}

@app.delete("/product/{id}")
def delete_products(id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    existing = db.query(models.Product).filter(models.Product.id == id).first()
    if not existing:
        return {"error": "product not found!"}
    db.delete(existing)
    db.commit()
    return {"message": "product deleted successfully!"}