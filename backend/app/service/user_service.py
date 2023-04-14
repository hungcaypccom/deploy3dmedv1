from app.model import Person, Users, UsersRole, Role

from app.repository.users import UsersRepository
from sqlalchemy.future import select
from app.config import db
from app.service import role_service


class UserService:

    async def find_account(account: str):
        info = await UsersRepository.find_by_username(account)
        return info

    async def find_account_all():
        info = await UsersRepository.get_all()
        return info

    @staticmethod
    async def get_user_profile_user(username):
        query = select(Users.username,
                        Person.name, 
                        Person.Date_start,
                        Person.Date_end,
                        Person.profile,
                        Person.phone_number,
                        Person.adress
                        ).join_from(Users,Person).where(Users.username == username)
        return(await db.execute(query)).mappings().one()


    async def get_user_profile_role_user(username):
        query = select(Users.username,
                        Person.name, 
                        Person.Date_start,
                        Person.Date_end,
                        Person.profile,
                        Person.phone_number,
                        Person.adress,
                        Users.source
                        ).join_from(Users,Person).where(Users.username == username)
        result =(await db.execute(query)).mappings().one()
        role = await role_service.find_role_by_username(username)
        result = dict(result)
        result["role"] = role.role_name
        return result
        
    
    @staticmethod
    async def get_account_all_by_role_user():
        role_id = await role_service.find_role_users("user")
        query = select(Users.username,
                        ).join_from(Users,UsersRole).where(UsersRole.role_id == role_id.id)
        return(await db.execute(query)).mappings().all()
    
    @staticmethod
    async def get_account_all_by_hans():
        return await UsersRepository.find_by_source("hans")

    @staticmethod
    async def update_source(username, source:str):
        return await UsersRepository.update_refresh_token(username, source)  

    @staticmethod
    async def update_refresh_token(username, token):
        return await UsersRepository.update_refresh_token(username, token)