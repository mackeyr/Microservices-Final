from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import APIKey
import secrets

router = APIRouter(prefix="/auth")

@router.post("/create_key")
def create_key(role: str, db: Session = Depends(get_db)):
    key = secrets.token_hex(16)
    obj = APIKey(key=key, role=role)
    db.add(obj)
    db.commit()
    return {"key": key, "role": role}
