from pydantic import BaseModel

class FactCreate(BaseModel):
    text: str
    source: str | None = None

class FactOut(BaseModel):
    id: int
    text: str
    source: str | None
    views: int
    score: int

    class Config:
        from_attributes = True


class APIKeyOut(BaseModel):
    key: str
    role: str
