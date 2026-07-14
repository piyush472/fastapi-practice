# FastAPI Product API

Backend project built while learning FastAPI. Started as a basic CRUD app and grew from there — added a real database, then authentication, then hooked up a simple frontend to see the whole thing work end to end.

## What it does

Product management API - add, view, update and delete products. Users can register and login, and get a JWT token back. Product routes are protected, so you need to be logged in to use them.

## Stack

- FastAPI
- PostgreSQL + SQLAlchemy
- JWT for auth (python-jose + passlib for password hashing)
- Pydantic for request validation
- Uvicorn

## Setup

Clone it:
git clone https://github.com/piyush472/fastapi-crud-project.git
cd fastapi-crud-project

Create a virtual environment and activate it:
python -m venv venv
venv\Scripts\activate
(use `source venv/bin/activate` if you're on mac/linux)

Install dependencies:
pip install -r requirements.txt

Create a `.env` file in the project root with your own database credentials:
DATABASE_URL=postgresql://postgres:yourpassword@localhost/product_api

Make sure PostgreSQL is running and you've created a database matching the name in your `.env` (e.g. `product_api`), either through pgAdmin or the command line.

Run the app:
uvicorn main:app --reload

Open `http://127.0.0.1:8000/docs` to test all the routes from the built-in Swagger UI. To test protected routes, first register and login to get a token, then click the **Authorize** button and paste `Bearer <your_token>`.

## Routes

**Auth**
- POST /register - create a user
- POST /login - get a JWT token

**Products** (need to be logged in, pass token via Authorize button in /docs)
- GET /products - get all products
- GET /products/{id} - get one product
- POST /product - add a product
- PUT /product/{id} - update a product
- DELETE /product/{id} - delete a product

## How auth works here

Password gets hashed before saving (never stored as plain text). On login, if credentials match, you get back a JWT token. That token has to be sent in the Authorization header for the product routes to work, otherwise you get a 401.

## Notes

Started this to actually understand backend concepts hands-on instead of just watching tutorials - CRUD, working with a real database instead of hardcoded data, and how auth actually works under the hood. Still improving it as I learn more.