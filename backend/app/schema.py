

from fastapi import HTTPException
import logging
import re
from typing import TypeVar, Optional

from pydantic import BaseModel, validator
from sqlalchemy import false
from datetime import date


T = TypeVar('T')

# get root logger
logger = logging.getLogger(__name__)


class RegisterSchema(BaseModel):

    # mapping request data to class entity table    
    username: str
    password: str
    name: str
    Date_start: str
    Date_end: str
    profile: str
    phone_number: str
    adress: str
    role: str
    source: str
   
    # phone number validation

class UpdateSchema(BaseModel):

    # mapping request data to class entity table    
    username: str
    password: str
    name: str
    Date_start: str
    Date_end: str
    profile: str
    phone_number: str
    adress: str
   
class UpdateUserSchema(BaseModel):

    # mapping request data to class entity table  
        name: str
        profile: str
        phone_number: str
        adress: str
  

class LoginSchema(BaseModel):
    username: str
    password: str

class ForgotPasswordSchema(BaseModel):
    username: str
    new_password: str

class ForgotPasswordSchemaUser(BaseModel):
    old_password: str
    new_password: str


class DetailSchema(BaseModel):
    status: str
    message: str
    result: Optional[T] = None

"""class ResponseSchema(BaseModel):
    detail : str
    result: Optional[T] = None"""

class ResponseSchema(BaseModel):
    detail: dict
    result: Optional[T] = None


class DeleteDataListSchema(BaseModel):
    dataList = list[str]

