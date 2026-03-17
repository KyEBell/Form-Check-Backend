from sqlmodel import SQLModel, Field
from typing import Optional


class Video(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    note: Optional[str] = None
    recorded_at: Optional[str] = None
