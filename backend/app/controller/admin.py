from fastapi import APIRouter,Depends,Security, Response
from app.client_download import client_download
from app.schema import ResponseSchema, RegisterSchema, LoginSchema, ForgotPasswordSchema
from app.repository.auth_repo import JWTBearer, JWTRepo, JWTBearerAdmin
from fastapi.security import HTTPAuthorizationCredentials
from app.service.user_service import UserService
from app.service.person_service import PersonService
from app.service import role_service
from app.schema import ResponseSchema, RegisterSchema, LoginSchema, ForgotPasswordSchema, UpdateSchema
from app.service.auth_service import AuthService
from app.service import info_data_service
from app.middleware.middleware import CookieAuth_RefreshToken_Admin, Cookie_Auth_Admin

router = APIRouter(
    prefix="/admin",
    tags=['admin'],
    dependencies=[Depends(Cookie_Auth_Admin())]
)

@router.get("/", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_user_profile(credentials= Security(Cookie_Auth_Admin())):
    result = await UserService.get_user_profile_user(credentials["username"])
    return ResponseSchema(detail={"status":"Successfully", "message":"Successfully get user" }, result=result)

@router.post("/register", response_model=ResponseSchema, response_model_exclude_none=True)
async def register(request_body: RegisterSchema):
    await AuthService.register_service(request_body)
    return ResponseSchema(detail={"status":"Successfully", "message":"Successfully regiester user" })

@router.post("/update-user-details", response_model=ResponseSchema, response_model_exclude_none=True)
async def register(request_body: RegisterSchema):
    await PersonService.update_person(request_body)
    return ResponseSchema(detail={"status":"Successfully", "message":"Successfully update user" })

@router.post("/forgot-password", response_model=ResponseSchema, response_model_exclude_none=True)
async def forgot_password(request_body: ForgotPasswordSchema):
    await AuthService.forgot_password_service(request_body)
    return ResponseSchema(detail={"status":"Successfully", "message":"Successfully update password" })

@router.post("/chage-status-infoData")
async def chageStatusInfoData(uploadTimeStr,status:bool ,downloadable:bool):
    await info_data_service.InFoDataService.update_status_downloadable(uploadTimeStr, status, downloadable)
    return ResponseSchema(detail={"status":"Successfully", "message":"Successfully changed" })

@router.post("/find-infoData")
async def findInfoData(uploadTimeStr):
    result = await info_data_service.InFoDataService.find_by_str(uploadTimeStr)
    return ResponseSchema(detail={"status":"Successfully", "message":"Successfully find infodata" }, result= result)

@router.post("/find-info-data-by-status")
async def findstatus(status:bool):
    result = await info_data_service.InFoDataService.find_by_status(status)
    return ResponseSchema(detail={"status":"Successfully", "message":"Successfully find infodata by status" }, result= result)


@router.post("/find-info-data-by-downloadable")
async def findstatus(downloadable:bool):
    result = await info_data_service.InFoDataService.find_by_downloadable(downloadable)
    return ResponseSchema(detail={"status":"Successfully", "message":"Successfully find infodata by downloadable" }, result= result) 

@router.get("/get-all-account")
async def getallaccount():
    result = await UserService.find_account_all()
    return ResponseSchema(detail={"status":"Successfully", "message":"Successfully get all account" }, result= result)

@router.post("/update-data-info-by-user")
async def updatedatainfobyuser(username, status:bool, downloadable: bool):
    results = await info_data_service.InFoDataService.find_by_user(username)
    for result in results:
        await info_data_service.InFoDataService.update_status_downloadable(result.uploadTimeStr, status, downloadable)
    return ResponseSchema(detail={"status":"Successfully", "message":"Successfully update infodata" })


@router.get("/data-info-find-all")
async def datainfofindall():
    result = await info_data_service.InFoDataService.find_all()
    return ResponseSchema(detail={"status":"Successfully", "message":"Successfully get all infodata" }, result=result)


@router.get("/user_details", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_user_profile(username):
    result = await UserService.get_user_profile_role_user(username)
    return ResponseSchema(detail={"status":"Successfully", "message":"Successfully get user details" }, result=result)


@router.get("/user_all")
async def getallaccount():
    accounts = await UserService.find_account_all()
    results = []
    for account in accounts:
        result = await UserService.get_user_profile_role_user(account.username)
        results.append(result)
    return ResponseSchema(detail={"status":"Successfully", "message":"Successfully get all users" }, result=results)

@router.post("/delete-file")
async def delete_file(response: Response, datalist: list[str], username):
    result = await client_download.client_delete_file(datalist, username)
    return ResponseSchema(detail={"status":"Successfully", "message":"Successfully delete files" }, result=result)


@router.get("/data-info-total-count",response_model=ResponseSchema, response_model_exclude_none=True)
async def data_info_total_count(downloadable:bool, username):
    result = await info_data_service.InFoDataService.find_by_user_total_count(username, downloadable)
    return ResponseSchema(detail={"status":"Successfully", "message":"Successfully get total count" }, result=result)
    
@router.get("/data-info-pagging",response_model=ResponseSchema, response_model_exclude_none=True)
async def data_info_pagging(downloadable:bool, page:int, count:int, username ):
    result = await info_data_service.InFoDataService.find_by_user_pagging(username, page, count, downloadable)
    return ResponseSchema(detail={"status":"Successfully", "message":"Successfully get data" }, result=result)