
from multiprocessing import synchronize
from sqlalchemy import update as sql_update
from sqlalchemy.future import select
from sqlalchemy import update as sql_update, delete as sql_delete, func, desc
from app.config import db, commit_rollback

from app.config import db, commit_rollback
from app.model.info_data import InfoData
from app.repository.base_repo import BaseRepo


class InfoDataRepository(BaseRepo):
    model = InfoData

    @staticmethod
    async def find_by_uploadTimeStr(uploadTimeStr: str):
        query = select(InfoData).where(InfoData.uploadTimeStr == uploadTimeStr)
        return (await db.execute(query)).scalar_one_or_none()
  
    
    @staticmethod
    async def find_by_user_id(user_id):
        query = select(InfoData).where(InfoData.user_id == user_id)
        return (await db.execute(query)).scalars().all()
    
    @staticmethod
    async def find_by_status(status):
        query = select(InfoData).where(InfoData.status == status)
        return (await db.execute(query)).scalars().all()
    

    @staticmethod
    async def delete_by_uploadTimeStr(uploadTimeStr: str):
        query = sql_delete(InfoData).where(InfoData.uploadTimeStr == uploadTimeStr)
        await db.execute(query)
        await commit_rollback()
    

    @staticmethod
    async def find_by_downloadable(downloadable):
        query = select(InfoData).where(InfoData.downloadable == downloadable)
        return (await db.execute(query)).scalars().all()
    
    @staticmethod
    async def update_status_downloadable(uploadTimeStr, status, downloadable):
        query = sql_update(InfoData).where(InfoData.uploadTimeStr == uploadTimeStr).values(
            status=status).values(downloadable=downloadable).execution_options(synchronize_session="fetch")
        await db.execute(query)
        await commit_rollback()

    @staticmethod
    async def find_by_user_id_total_count(username, downloadable:bool):
        if downloadable == True:
            query =  select(func.count(InfoData.id)).where(InfoData.accountNo==username  , InfoData.downloadable == downloadable)
        else:
            query =  select(func.count(InfoData.id)).where(InfoData.accountNo==username)
        return (await db.execute(query)).scalar()
                
    async def find_by_user_id_pagging(username, page, count, downloadable:bool):
        try:
            if downloadable == True:
                skip = count * (page - 1)
                query = select(InfoData).order_by((InfoData.created_at).desc()).filter(InfoData.downloadable == downloadable,InfoData.accountNo==username ).offset(skip).limit(count)
            else:
                skip = count * (page - 1)
                query = select(InfoData).order_by((InfoData.created_at).desc()).filter(InfoData.accountNo==username ).offset(skip).limit(count)
            #query = select(InfoData).where(InfoData.accountNo == username).offset(skip).limit(count)
            return (await db.execute(query)).scalars().all()
        except Exception as e:
            print("error in find_by_user_id_pagging", e)
    
    async def find_by_user_id_2_last(username, count):
        query = select(InfoData.uploadTimeStr).order_by((InfoData.created_at).desc()).filter(InfoData.accountNo==username).limit(count)
        return (await db.execute(query)).scalars().all()