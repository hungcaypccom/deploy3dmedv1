from app.model.user_role import UsersRole
from app.repository.base_repo import BaseRepo
from typing import List
from sqlalchemy.future import select
from sqlalchemy import update as sql_update

from app.config import db,commit_rollback

class UsersRoleRepository(BaseRepo):
    model = UsersRole

    @staticmethod
    async def find_by_user_id(user_id:str):
        query = select(UsersRole).where(UsersRole.users_id == user_id)
        return (await db.execute(query)).scalar_one_or_none()

    @staticmethod
    async def update_by_user_id(user_id:str, role_id: str):
        query = sql_update(UsersRole).where(UsersRole.users_id == user_id).values(
            role_id = role_id).execution_options(synchronize_session="fetch")
        await db.execute(query)
        await commit_rollback()
