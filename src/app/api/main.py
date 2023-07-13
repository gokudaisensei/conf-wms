from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import users, auth, institutions

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(institutions.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def pong():
    return {"ping": "pong!"}