import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from fastapi import Query


def get_db():
    engine = create_engine(os.getenv('DATABASE_URL')) # type: ignore

    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

def get_pagination_params(
    # page must be greater than 0
    page: int = Query(1, gt=0),
    # per_page must be greater than 0
    per_page: int = Query(10, gt=0)
):
    return {"page": page, "per_page": per_page}
