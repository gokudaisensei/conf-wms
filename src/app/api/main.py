from fastapi import FastAPI
from app.api.routers import users, auth

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/ping")
def pong():
    return {"ping": "pong!"}