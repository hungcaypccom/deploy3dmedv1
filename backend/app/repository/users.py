
import email
from multiprocessing import synchronize
from sqlalchemy import update as sql_update
from sqlalchemy.future import select


from app.config import db, commit_rollback
from app.model.users import Users
from app.model.person import Person
from app.repository.base_repo import BaseRepo


class UsersRepository(BaseRepo):
    model = Users

    @staticmethod
    async def find_by_username(username: str):
        query = select(Users).where(Users.username == username)
        return (await db.execute(query)).scalar_one_or_none()

    @staticmethod
    async def update_password(username: str, password: str):
        query = sql_update(Users).where(Users.username == username).values(
            password=password).execution_options(synchronize_session="fetch")
        await db.execute(query)
        await commit_rollback()

    @staticmethod
    async def update_refresh_token(username: str, token: str):
        query = sql_update(Users).where(Users.username == username).values(
            rf_tocken=token).execution_options(synchronize_session="fetch")
        await db.execute(query)
        await commit_rollback()


    @staticmethod
    async def update_source(username: str, source: str):
        query = sql_update(Users).where(Users.username == username).values(
            source=source).execution_options(synchronize_session="fetch")
        await db.execute(query)
        await commit_rollback()

    @staticmethod
    async def find_by_source(source: str):  
        query = select(Users).where(Users.source == source)
        return (await db.execute(query)).scalars().all()