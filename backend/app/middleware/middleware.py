from fastapi import Request, HTTPException, Cookie

from app.repository.auth_repo import JWTRepo
from app.service.user_service import UserService
from fastapi import Request
from fastapi_limiter.depends import RateLimiter
from app.middleware.config import Rate_limit_times, Rate_limit_seconds


class Rate_Limiter():
    def __init__(self, time = Rate_limit_times, seconds = Rate_limit_seconds ) -> None:
        self.time = time
        self.seconds = seconds
        pass
    def __call__(self, request: Request):
        RateLimiter(self.time, self.seconds)
        print("in ratelimit")

class Cookie_Auth(): 
    def __call__(self, request: Request):
        credentials = request.cookies.get("access_token")
        if credentials:
            token = JWTRepo(token = credentials).decode_access_token()
            return token
        else:
            raise HTTPException (
            status_code=401, detail={"status": "Unauthorized", "message": "Missing authorization token"}
            )
        
class CookieAuth_RefreshToken(): 
    async def __call__(self, request: Request):
        credentials = request.cookies.get("refresh_token")
        if credentials:
            token = JWTRepo(token = credentials).decode_refresh_token()
            rf_token_database = await UserService.find_account(token["username"])
            if rf_token_database.rf_tocken == credentials:
                return token
            else:
                raise HTTPException (
                status_code=403, detail={"status": "Forbidden", "message": "Old refresh token!"}
                )
        else:
            raise HTTPException (
            status_code=401, detail={"status": "Unauthorized", "message": "Missing refresh token"}
            )

class Cookie_Auth_Admin(): 
    def __call__(self, request: Request):
        credentials = request.cookies.get("access_token")
        if credentials:
            token = JWTRepo(token = credentials).decode_access_token()
            try:
                if token["role"] == "admin":
                    return token
            except:
                raise HTTPException (
                status_code=403, detail={"status": "Forbidden", "message": "Using user's token"}
                )
        else:
            raise HTTPException (
            status_code=401, detail={"status": "Unauthorized", "message": "Missing authorization token"}
            )
        
class CookieAuth_RefreshToken_Admin(): 
    async def __call__(self, request: Request):
        credentials = request.cookies.get("refresh_token")
        if credentials:
            token = JWTRepo(token = credentials).decode_refresh_token()
            if token["role"] != "admin":     
                raise HTTPException (
                status_code=403, detail={"status": "Forbidden", "message": "Using user's token"}
                                    )
            rf_token_database = await UserService.find_account(token["username"])
            if rf_token_database.rf_tocken == credentials:
                return token
            else:
                raise HTTPException (
                status_code=403, detail={"status": "Forbidden", "message": "Old refresh token!"}
                )
        else:
            raise HTTPException (
            status_code=401, detail={"status": "Unauthorized", "message": "Missing refresh token"}
            )
        