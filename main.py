from fastapi import FastAPI

app=FastAPI()

@app.get("/") #decorator used to define end point
def home():
    return {"message":"hello"}