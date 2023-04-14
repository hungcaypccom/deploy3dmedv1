from fastapi import APIRouter,  Cookie, Depends
from fastapi.responses import Response
from app.schema import ResponseSchema, RegisterSchema, LoginSchema, ForgotPasswordSchema
from app.service.auth_service import AuthService
from app.middleware.middleware import CookieAuth_RefreshToken, CookieAuth_RefreshToken_Admin, Rate_Limiter
from fastapi import Security


router = APIRouter(prefix="/auth", tags=['Authentication'], 
                    dependencies=[Depends(Rate_Limiter())]
                                 
                    )



@router.post("/login", response_model=ResponseSchema, response_model_exclude_none=True)
async def login_user(requset_body: LoginSchema, responses: Response):
    token = await AuthService.logins_service(requset_body)
    responses.set_cookie(key="access_token", value=token["access_token"], httponly=True, samesite="strict")
    responses.set_cookie(key="refresh_token", value=token["refresh_token"], httponly=True, samesite="strict")
    return ResponseSchema(detail={"status": "Successfully", "message": "Successfully login"})

@router.post("/admin", response_model=ResponseSchema, response_model_exclude_none=True)
async def login_admin(requset_body: LoginSchema, responses: Response):
    token = await AuthService.logins_service_admin(requset_body)
    responses.set_cookie(key="access_token", value=token["access_token"], httponly=True, samesite="strict")
    responses.set_cookie(key="refresh_token", value=token["refresh_token"], httponly=True, samesite="strict")
    return ResponseSchema(detail={"status": "Successfully", "message": "Successfully login"})

@router.post("/refresh-token", response_model=ResponseSchema, response_model_exclude_none=True)
async def refresh_token( responses: Response, credentials= Security(CookieAuth_RefreshToken())):
    token = await AuthService.refresh_token(credentials["username"])
    responses.set_cookie(key="access_token", value=token["access_token"], httponly=True, samesite="strict")
    return ResponseSchema(detail={"status": "Successfully", "message": "Successfully refresh token"})

@router.post("/refresh-token-admin", response_model=ResponseSchema, response_model_exclude_none=True)
async def refresh_token_admin( responses: Response, credentials= Security(CookieAuth_RefreshToken_Admin())):
    token = await AuthService.refresh_token_admin(credentials["username"])
    responses.set_cookie(key="access_token", value=token["access_token"], httponly=True, samesite="strict")
    return ResponseSchema(detail={"status": "Successfully", "message": "Successfully refresh token"})
