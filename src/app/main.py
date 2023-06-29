from fastapi import FastAPI
from app.routers import users
import os, sys

app = FastAPI()
app.include_router(users.router)

@app.get("/ping")
def pong():
    return {"ping": "pong!"}