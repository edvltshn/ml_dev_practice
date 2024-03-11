# from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlmodel import Column, DateTime, Field, SQLModel, func, String, Relationship


class Task(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now()))
    predicted_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))
    predictor: Optional[str] = Field(default=None, sa_column=Column(String, nullable=True), foreign_key="predictor.name")
    input_data: str
    output_data: Optional[str] = Field(default=None, sa_column=Column(String, nullable=True))
    user: "User" = Relationship(back_populates="tasks")
