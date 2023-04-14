from typing import List, Optional
from sqlalchemy import Column, String
from sqlmodel import SQLModel, Field, Relationship

from app.model.mixins import TimeMixin


class InfoData(SQLModel,TimeMixin,table=True):
    __tablename__= "infodata"

    id: Optional[str] = Field(None, primary_key=True, nullable=False)

    accountNo: str
    uploadTimeStr: str
    fileSize: str
    createTime: str
    name: str
    birthday: str
    phone: str
    sex: str
    status: Optional[bool] = Field(default=True)
    downloadable: Optional[bool] = Field(default=False)
    

    user_id: Optional[str] = Field(default=None, foreign_key="users.id")
    userIF: Optional["Users"]  = Relationship(back_populates="infos")