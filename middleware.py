from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException
from starlette.requests import Request
import json

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/docs", "/openapi.json", "/auth/authenticate"]:
            response = await call_next(request)
            return response
        
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="Missing Authorization header")
        
        try:
            auth_data = json.loads(auth_header)
            request.state.auth = auth_data
        except json.JSONDecodeError:
            raise HTTPException(status_code=401, detail="Invalid Authorization header format")
        
        response = await call_next(request)
        return response
