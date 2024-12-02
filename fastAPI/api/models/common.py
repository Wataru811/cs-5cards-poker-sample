import datetime

from pydantic import BaseModel, Field, validator


# non-null-value dict
def classToDictByNNV(cls):
    result = {}
    for key, value in cls.__dict__.items():
        if not key.startswith('__') and value is not None:
            result[key] = value
    return result



class CvModel( BaseModel ):
    owner: str
    uuid: str
    created_at: datetime.datetime = None  # type: ignore
    updated_at: datetime.datetime = None  # type: ignore

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(
        cls,  
        value: datetime.datetime, 
    ) -> datetime.datetime:
        return value or datetime.datetime.now()


class CvSchema( BaseModel ):
    owner: str
    uuid: str
    created_at: datetime.datetime = None  # type: ignore
    updated_at: datetime.datetime = None  # type: ignore

  

class DateTimeModelMixin(BaseModel):
    created_at: datetime.datetime = None  # type: ignore
    updated_at: datetime.datetime = None  # type: ignore

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(
        cls,  # noqa: N805
        value: datetime.datetime,  # noqa: WPS110
    ) -> datetime.datetime:
        return value or datetime.datetime.now()


class IDModelMixin(BaseModel):
    id_: int = Field(0, alias="id")


#class Dataset(SQLModel, table=True):
#    id: uuid.UUID = Field(default=None, primary_key=True)


# ---------------------- schema -------------------
class mdlIdList(BaseModel):
    ids: list[str] = []





"""
from typing import List

class RWSchema(RWModel):
    class Config(RWModel.Config):
        orm_mode = True

class ListOfCommentsInResponse(RWSchema):
    comments: List[Comment]

class CommentInResponse(RWSchema):
    comment: Comment

class CommentInCreate(RWSchema):
    body: str
"""