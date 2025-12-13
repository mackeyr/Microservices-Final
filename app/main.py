from fastapi import FastAPI
from .stats_middleware import StatsMiddleware
from .database import Base, engine
from .routers import facts, admin, auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(StatsMiddleware)

app.include_router(facts.router)
app.include_router(admin.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Fun Fact Generator running"}
