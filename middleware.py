from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException, Depends
from starlette.requests import Request
import json
from dao.user_dao import UserDAO
from configurations.config import SessionLocal

class AuthMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)
        
        if request.url.path in ["/docs", "/openapi.json", "/auth/authenticate"]:
            response = await call_next(request)
            return response
        
        token_header = request.headers.get("Authorization")
        print("Headers: ", request.headers)
        if not token_header:
            raise HTTPException(status_code=401, detail="Missing Authorization header")
        
        token_data = token_header.split('#-%')
        with SessionLocal() as db:
            user = UserDAO.get_user_by_id(db, token_data[1])

            if not any(ua.accesstoken_id == token_data[0] for ua in user.user_accesses):
                raise HTTPException(status_code=403, detail="Invalid Token")
            
            if not any(sa.id == token_data[2] for sa in user.sources):
                raise HTTPException(status_code=403, detail="Invalid Token")
    
        try:
            auth_data = {
                "auth": {
                "access_tokens": [token_data[0]],
                "sources": [token_data[2]],
                "user_id": token_data[1]
                }
            }
            request.state.auth = auth_data            
            response = await call_next(request)
            return response                    
        except Exception:
            raise HTTPException(status_code=403, detail="Invalid request")
            
