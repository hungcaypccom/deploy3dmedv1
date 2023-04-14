import base64
from datetime import datetime, date
from uuid import uuid4
from fastapi import HTTPException

from app.model import Person, Users, UsersRole, Role
from app.repository.role import RoleRepository
from app.repository.users import UsersRepository
from app.repository.person import PersonRepository
from app.repository.user_role import UsersRoleRepository

from passlib.context import CryptContext
from app.schema import RegisterSchema
from app.schema import LoginSchema, ForgotPasswordSchema
from app.repository.auth_repo import JWTRepo
from app.service import role_service
from app.service.user_service import UserService


# Encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:

    @staticmethod
    async def register_service(register: RegisterSchema):

        # Create uuid
        _person_id = str(uuid4())
        _users_id = str(uuid4())

        # convert date type from frontend str to date
        try:
            Date_start = datetime.strptime(register.Date_start, '%d-%m-%Y')
            Date_end = datetime.strptime(register.Date_end, '%d-%m-%Y')
        except: 
            raise HTTPException(
                status_code=400, detail={"status": "Bad Request", "message": "Wrong date time format"}
            )
        password = pwd_context.hash(register.password)
        # open image profile default to bas64 string


        # mapping request data to class entity table
        _person = Person(id=_person_id, name=register.name, Date_start=Date_start, 
    Date_end=Date_end, profile=register.profile, phone_number=register.phone_number, adress=register.adress)

        _users = Users(id=_users_id, username=register.username, 
                       password=password, source=register.source,
                       person_id=_person_id)
        try:
            _role = await RoleRepository.find_by_role_name(register.role)
            _users_role = UsersRole(users_id=_users_id, role_id=_role.id)
        except:
            raise HTTPException(
                status_code=400, detail={"status": "Bad Request", "message": "Wrong role farmat"}
            )

        # Cheking the same username
        _username = await UsersRepository.find_by_username(register.username)
        if _username:
            raise HTTPException(
                status_code=400, detail="Username already exists!")
        else:
            #  insert to tables
            await PersonRepository.create(**_person.dict())
            await UsersRepository.create(**_users.dict())
            await UsersRoleRepository.create(**_users_role.dict())



    @staticmethod
    async def logins_service(login: LoginSchema):
        _username = await UsersRepository.find_by_username(login.username)
        if _username is not None:
            person = await UserService.get_user_profile_user(login.username)
            if person.Date_end < date.today():
               raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Account Expired!"})
            if not pwd_context.verify(login.password, _username.password):
                raise HTTPException(
                    status_code=400, detail={"status": "Bad Request", "message": "Invalid password"})
            token = { "access_token": JWTRepo(data={"username": _username.username}).generate_access_token()
                     , "refresh_token": JWTRepo(data={"username": _username.username}).generate_refresh_token()
                    }
            await UserService.update_refresh_token(login.username, token["refresh_token"])
            return token
        raise HTTPException(status_code=404, detail={"status": "Not Found", "message": "Username not Found"})



    @staticmethod
    async def logins_service_admin(login: LoginSchema):
        _username = await UsersRepository.find_by_username(login.username)
        if _username is not None:
            person = await UserService.get_user_profile_user(login.username)
            if person.Date_end < date.today():
               raise HTTPException(
                    status_code=403, detail={"status": "Forbidden", "message": "Account Expired!"})
            result = await role_service.find_role_by_user_id(_username.id)
            if (result.role_name == "admin"):
                if not pwd_context.verify(login.password, _username.password):
                    raise HTTPException(
                    status_code=400, detail={"status": "Bad Request", "message": "Invalid password"})
                token = { "access_token": JWTRepo(data={"username": _username.username, "role":"admin"}).generate_access_token()
                     , "refresh_token": JWTRepo(data={"username": _username.username, "role": "admin"}).generate_refresh_token()
                    }
                await UserService.update_refresh_token(login.username, token["refresh_token"])
                return token
            raise HTTPException(status_code=403, detail={"status": "Forbidden", "message": "You are not Admin"})
        raise HTTPException(status_code=404, detail={"status": "Not Found", "message": "Username not Found"})
    
    @staticmethod
    async def refresh_token(username):
        new_token = { "access_token": JWTRepo(data={"username": username}).generate_access_token()
                    }
        return new_token

    @staticmethod
    async def refresh_token_admin(username):
        new_token = { "access_token": JWTRepo(data={"username": username, "role":"admin"}).generate_access_token()
                    }
        return new_token

    @staticmethod
    async def forgot_password_service(forgot_password: ForgotPasswordSchema):
        _username = await UsersRepository.find_by_username(forgot_password.username)
        if _username is None:
            raise HTTPException(status_code=404, detail={"status":"Not Found", "message":"Username not found"})
        await UsersRepository.update_password(forgot_password.username, pwd_context.hash(forgot_password.new_password))


    # Generate roles manually
    @staticmethod
    async def generate_role():
        _role = await RoleRepository.find_by_list_role_name(["admin", "user"])
        if not _role:
            await RoleRepository.create_list(
                [Role(id=str(uuid4()), role_name="admin"), Role(id=str(uuid4()), role_name="user")])
  


