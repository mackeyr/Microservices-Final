from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas
from ..auth import require_key

router = APIRouter(prefix="/facts")

@router.get("/random", response_model=schemas.FactOut)
def get_random_fact(db: Session = Depends(get_db)):
    fact = crud.get_random_fact(db)
    if not fact:
        return {"id": 0, "text": "No facts available", "source": None, "views": 0, "score": 0}
    fact.views += 1
    db.commit()
    return fact

@router.post("/", response_model=schemas.FactOut)
def create_fact(fact: schemas.FactCreate, key = Depends(require_key), db: Session = Depends(get_db)):
    return crud.create_fact(db, fact)
