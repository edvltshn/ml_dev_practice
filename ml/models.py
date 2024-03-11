from datetime import datetime
from typing import Optional
from sqlmodel import Column, DateTime, Field, SQLModel, func, String, Text

class BaseModel(SQLModel):
    id: int = Field(primary_key=True)

class User(BaseModel, table=True):
    email: str = Text()
    password: str = Text()
    user_token: str = Field(unique=True)
    blance: int = Field(default=500)
    name: str = Field(default=None, nullable=True)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)

class Predictor(BaseModel, table=True):
    name: str = Field(unique=True)
    cost: int = Field()
    is_active: bool = Field(default=True)

class Task(SQLModel, table=True):
    id: int = Field(primary_key=True)
    predicted_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))
    input_data: str
    output_data: Optional[str] = Field(default=None, sa_column=Column(String, nullable=True))

