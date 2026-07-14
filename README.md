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

