from fastapi import APIRouter,Depends,Security, Response, Body

from app.schema import ResponseSchema, UpdateUserSchema, DeleteDataListSchema, ForgotPasswordSchemaUser
from app.repository.auth_repo import JWTBearer, JWTRepo
from app.middleware.middleware import Cookie_Auth, Rate_Limiter
from fastapi.security import HTTPAuthorizationCredentials
from app.service.user_service import UserService
from app.service import  info_data_service, person_service

from app.client_download import client_download


router = APIRouter(
    prefix="/users",
    tags=['user'],
    dependencies=[Depends(Cookie_Auth())]
)


@router.get("/", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_user_profile(credentials= Security(Cookie_Auth())):
    result = await UserService.get_user_profile_user(credentials["username"])
    return ResponseSchema(detail={"status":"Successfully", "message":"Successfully get user" }, result=result)

@router.post("/edit-profile", response_model=ResponseSchema, response_model_exclude_none=True)
async def edit_profile(request_body: UpdateUserSchema, credentials= Security(Cookie_Auth())):
    result = await person_service.PersonService.update_person_user(request_body, credentials["username"])
    return ResponseSchema(detail={"status":"Successfully", "message":"Successfully updated profile" }, result=result)

@router.post("/change-password", response_model=ResponseSchema, response_model_exclude_none=True)
async def edit_profile(request_body: ForgotPasswordSchemaUser, credentials= Security(Cookie_Auth())):
    result = await person_service.PersonService.update_password(request_body, credentials["username"])
    return ResponseSchema(detail={"status":"Successfully", "message":"Successfully updated password" }, result=result)

@router.post("/download-file", response_model=ResponseSchema, response_model_exclude_none=True)
async def download_file(response: Response, uploadTimeStr: str = Body(...), credentials= Security(Cookie_Auth())):
    result = await client_download.client_download_file(Response, uploadTimeStr, credentials["username"])
    return ResponseSchema(detail={"status":"Successfully", "message":"Successfully download file" }, result=result)

@router.get("/data-info-total-count",response_model=ResponseSchema, response_model_exclude_none=True)
async def data_info_total_count(downloadable:bool, credentials= Security(Cookie_Auth())):
    result = await info_data_service.InFoDataService.find_by_user_total_count(credentials['username'], downloadable)
    return ResponseSchema(detail={"status":"Successfully", "message":"Successfully got total count" }, result=result)
    
@router.get("/data-info-pagging",response_model=ResponseSchema, response_model_exclude_none=True)
async def data_info_pagging(downloadable:bool, page:int, count:int, credentials= Security(Cookie_Auth())):
    result = await info_data_service.InFoDataService.find_by_user_pagging(credentials['username'], page, count, downloadable)
    return ResponseSchema(detail={"status":"Successfully", "message":"Successfully got data" }, result=result)

@router.post("/delete-file", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_file(response: Response, datalist: list[str], credentials= Security(Cookie_Auth())):
    result = await client_download.client_delete_file(datalist, credentials["username"])
    return ResponseSchema(detail={"status":"Successfully", "message":"Successfully delete data" }, result=result)
