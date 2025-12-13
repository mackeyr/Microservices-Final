from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .crud import get_api_key

def require_key(x_api_key: str = Header(None), db: Session = Depends(get_db)):
    if not x_api_key:
        raise HTTPException(401, "Missing API key")
    key_obj = get_api_key(db, x_api_key)
    if not key_obj:
        raise HTTPException(403, "Invalid API key")
    return key_obj

def require_admin(key_obj = Depends(require_key)):
    if key_obj.role != "admin":
        raise HTTPException(403, "Admin role required")
    return key_obj
