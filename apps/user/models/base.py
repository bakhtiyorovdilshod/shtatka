import sqlalchemy
from sqlalchemy.sql import func
from pydantic import BaseModel
from datetime import datetime


def base_model():
    id = sqlalchemy.Column('id', sqlalchemy.INTEGER, primary_key=True)
    created_date = sqlalchemy.Column('created_date', sqlalchemy.DateTime, server_default=func.now())
    updated_date = sqlalchemy.Column('updated_date', sqlalchemy.DateTime, server_onupdate=func.now())
    is_deleted = sqlalchemy.Column('is_deleted', sqlalchemy.Boolean, default=False)
    return [id, created_date, updated_date, is_deleted]


class BaseSchema(BaseModel):
    id: int
    created_date: datetime
    updated_date: datetime
    is_deleted: bool
