from typing import Annotated, Optional

from fastapi import Cookie, FastAPI
from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4

class Cookies(BaseModel):
    session_id: str 
    fatebook_tracker: str 
    googall_tracker: str 


class CookieBase(SQLModel, table=True):
    session_id: str = Field(default="123")
    fatebook_tracker: str = Field(default="123")
    googall_tracker: str = Field(default="123")
    uuid:Optional[UUID] = Field(default_factory=uuid4, primary_key=True)