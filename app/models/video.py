from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone


class Video(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    note: Optional[str] = None
    recorded_on: Optional[str] = None
    updated_on: Optional[datetime] = None
    uploaded_on: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
