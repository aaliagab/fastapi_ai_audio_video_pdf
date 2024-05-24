from starlette.middleware.base import BaseHTTPMiddleware
from dao.access_dao import AccessDAO
from fastapi import Request, HTTPException

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        access_token = request.headers.get("Authorization")
        if not access_token:
            raise HTTPException(status_code=401, detail="Missing access token")

        access_token = access_token.replace("Bearer ", "")
        db = request.app.state.db
        access = AccessDAO.get_access_by_id(db, access_token)
        if not access:
            raise HTTPException(status_code=403, detail="Invalid access token")

        request.state.access = access
        response = await call_next(request)
        return response
