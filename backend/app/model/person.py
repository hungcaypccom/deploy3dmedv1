

from datetime import date
from typing import Optional
from sqlalchemy import Enum, table
from sqlmodel import SQLModel, Field, Relationship
from app.model.mixins import TimeMixin



class Person(SQLModel, TimeMixin, table=True):
    __tablename__ = "person"

    id: Optional[str] = Field(None, primary_key=True, nullable=False)
    name: str
    Date_start: Optional[date] = Field(nullable=False)
    Date_end: Optional[date] = Field(nullable=False)
    profile: Optional[str] = Field(nullable=True)
    phone_number: str
    adress: str

    users: Optional["Users"] = Relationship(
        sa_relationship_kwargs={'uselist': False}, back_populates="person")
