from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from .database import SessionLocal
from .crud import record_usage

class StatsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        db = SessionLocal()
        try:
            api_key = request.headers.get("x-api-key")
            record_usage(
                db,
                endpoint=request.url.path,
                method=request.method,
                status_code=response.status_code,
                api_key=api_key
            )
        finally:
            db.close()

        return response
