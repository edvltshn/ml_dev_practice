from sqlmodel import Field, Text, Relationship 
from typing import List

from  model.base_model import BaseModel

class User(BaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str = Text()
    password: str = Text()
    user_token: str = Field(unique=True)
    blance: int = Field(default=500)
    name: str = Field(default=None, nullable=True)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    tasks: List["Task"] = Relationship(back_populates="user")

