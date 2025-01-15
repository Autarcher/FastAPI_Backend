from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from uuid import UUID, uuid4
class UserDetail(BaseModel):
    high: int
    weight: int = None

class User(SQLModel, table=True):
    name: str = Field(..., title="用户名", description="发起者的名字")
    age: int = Field(default=18, description="发起者的年龄")
    uuid: UUID = Field(default=uuid4, primary_key=True, description="唯一标识符")
    # detail: UserDetail = None
    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [
    #             {
    #                 "name": "Foo",
    #                 "age": 18,
    #                 "detail": {
    #                     "high": 180,
    #                     "weight": 70,
    #                 }
                    
    #             }
    #         ]
    #     }
    # }

class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None